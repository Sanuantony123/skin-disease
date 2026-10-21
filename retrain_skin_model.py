
import os
import json
import numpy as np
import tensorflow as tf

from pathlib import Path
from collections import Counter

# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

TRAIN_DIR = BASE_DIR / "dataset" / "SKIN" / "train"
TEST_DIR = BASE_DIR / "dataset" / "SKIN" / "test"

MODEL_DIR = BASE_DIR / "backend" / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# Keep the existing production model unchanged during training.
OUTPUT_MODEL = MODEL_DIR / "skin_disease_retrained_candidate.keras"
OUTPUT_CLASSES = MODEL_DIR / "class_names_retrained.json"

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 123

INITIAL_EPOCHS = 12
FINE_TUNE_EPOCHS = 15
FINE_TUNE_LAST_LAYERS = 30

tf.keras.utils.set_random_seed(SEED)

# ============================================================
# CHECK DATASET
# ============================================================

if not TRAIN_DIR.is_dir():
    raise FileNotFoundError(f"Training folder not found: {TRAIN_DIR}")

if not TEST_DIR.is_dir():
    raise FileNotFoundError(f"Testing folder not found: {TEST_DIR}")

print("=" * 65)
print("SKIN DISEASE MODEL RETRAINING")
print("=" * 65)

# ============================================================
# LOAD TRAINING AND VALIDATION DATA
# ============================================================

train_ds = tf.keras.utils.image_dataset_from_directory(
    str(TRAIN_DIR),
    labels="inferred",
    label_mode="int",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.20,
    subset="training",
    seed=SEED,
    shuffle=True,
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    str(TRAIN_DIR),
    labels="inferred",
    label_mode="int",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.20,
    subset="validation",
    seed=SEED,
    shuffle=False,
    class_names=train_ds.class_names,
)

CLASS_NAMES = list(train_ds.class_names)
NUM_CLASSES = len(CLASS_NAMES)

print("\nClass count:", NUM_CLASSES)

for index, name in enumerate(CLASS_NAMES):
    print(f"{index}: {name}")

if NUM_CLASSES != 23:
    raise ValueError(
        f"Expected 23 disease classes but found {NUM_CLASSES}. "
        "Check the training folder structure before continuing."
    )

# ============================================================
# LOAD TEST DATA USING THE SAME CLASS ORDER
# ============================================================

test_ds = tf.keras.utils.image_dataset_from_directory(
    str(TEST_DIR),
    labels="inferred",
    label_mode="int",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
    class_names=CLASS_NAMES,
)

# Do not cache the complete image dataset in RAM.
AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)
test_ds = test_ds.prefetch(AUTOTUNE)

# ============================================================
# CLASS IMBALANCE WEIGHTS
# ============================================================

class_counts = {}

for class_name in CLASS_NAMES:
    class_folder = TRAIN_DIR / class_name

    count = sum(
        1
        for path in class_folder.rglob("*")
        if path.is_file()
        and path.suffix.lower() in {
            ".jpg", ".jpeg", ".png", ".webp", ".bmp"
        }
    )

    class_counts[class_name] = count

if any(count == 0 for count in class_counts.values()):
    raise ValueError(
        "At least one training class has no supported images."
    )

total_images = sum(class_counts.values())

class_weights = {
    index: total_images / (NUM_CLASSES * class_counts[name])
    for index, name in enumerate(CLASS_NAMES)
}

print("\nTraining images per class:")
for name, count in class_counts.items():
    print(f"{name}: {count}")

print("\nClass weights:")
for index, name in enumerate(CLASS_NAMES):
    print(f"{name}: {class_weights[index]:.4f}")

# ============================================================
# DATA AUGMENTATION
# ============================================================

augmentation = tf.keras.Sequential(
    [
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.08),
        tf.keras.layers.RandomZoom(0.10),
        tf.keras.layers.RandomContrast(0.10),
    ],
    name="data_augmentation",
)

# ============================================================
# BUILD MODEL
# ============================================================

# Important:
# This model performs its own pixel scaling:
# 0..255 -> approximately -1..1.
#
# Therefore, when using this model in app.py, use:
# SKIN_PREPROCESSING=raw
#
# Do not also apply MobileNetV2 preprocess_input in Flask.

inputs = tf.keras.Input(
    shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
    name="image",
)

x = augmentation(inputs)

x = tf.keras.layers.Rescaling(
    scale=1.0 / 127.5,
    offset=-1.0,
    name="mobilenet_scaling",
)(x)

base_model = tf.keras.applications.MobileNetV2(
    include_top=False,
    weights="imagenet",
    input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3),
)

base_model.trainable = False

x = base_model(x, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.35)(x)

outputs = tf.keras.layers.Dense(
    NUM_CLASSES,
    activation="softmax",
    name="disease_predictions",
)(x)

model = tf.keras.Model(inputs, outputs)

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

model.summary()

# ============================================================
# CALLBACKS
# ============================================================

def create_callbacks():
    return [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(OUTPUT_MODEL),
            monitor="val_loss",
            save_best_only=True,
            mode="min",
            verbose=1,
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=4,
            restore_best_weights=True,
            verbose=1,
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.3,
            patience=2,
            min_lr=1e-7,
            verbose=1,
        ),
    ]


# ============================================================
# STAGE 1: TRAIN THE CLASSIFICATION HEAD
# ============================================================

print("\n" + "=" * 65)
print("STAGE 1: TRAINING CLASSIFICATION HEAD")
print("=" * 65)

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=INITIAL_EPOCHS,
    class_weight=class_weights,
    callbacks=create_callbacks(),
)

# Load the best stage-1 checkpoint before fine-tuning.
model = tf.keras.models.load_model(
    str(OUTPUT_MODEL),
    compile=False,
)

# ============================================================
# STAGE 2: FINE-TUNE THE LAST BASE-MODEL LAYERS
# ============================================================

print("\n" + "=" * 65)
print("STAGE 2: FINE-TUNING MOBILENETV2")
print("=" * 65)

# The loaded model's backbone is the third top-level layer:
# Input, augmentation, rescaling, backbone, pooling, dropout, output.
backbone = None

for layer in model.layers:
    if isinstance(layer, tf.keras.Model) and "mobilenetv2" in layer.name.lower():
        backbone = layer
        break

if backbone is None:
    # Find the nested model by its layer structure/name.
    for layer in model.layers:
        if isinstance(layer, tf.keras.Model):
            backbone = layer

if backbone is None:
    raise RuntimeError("Could not find the MobileNetV2 backbone.")

backbone.trainable = True

# Freeze most layers and fine-tune only the last portion.
for layer in backbone.layers:
    layer.trainable = False

for layer in backbone.layers[-FINE_TUNE_LAST_LAYERS:]:
    # Batch normalization layers are kept frozen for stability.
    if not isinstance(layer, tf.keras.layers.BatchNormalization):
        layer.trainable = True

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=FINE_TUNE_EPOCHS,
    class_weight=class_weights,
    callbacks=create_callbacks(),
)

# ============================================================
# LOAD BEST CHECKPOINT AND EVALUATE ON UNSEEN TEST DATA
# ============================================================

print("\n" + "=" * 65)
print("FINAL TEST EVALUATION")
print("=" * 65)

model = tf.keras.models.load_model(
    str(OUTPUT_MODEL),
    compile=False,
)

model.compile(
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"],
)

test_loss, test_accuracy = model.evaluate(
    test_ds,
    verbose=1,
)

print(f"\nTest loss: {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy * 100:.2f}%")

# ============================================================
# PER-CLASS TEST ACCURACY
# ============================================================

correct = np.zeros(NUM_CLASSES, dtype=np.int64)
total = np.zeros(NUM_CLASSES, dtype=np.int64)

for images, labels in test_ds:
    outputs = model.predict(images, verbose=0)
    predictions = np.argmax(outputs, axis=1)
    labels = labels.numpy()

    for actual, predicted in zip(labels, predictions):
        total[int(actual)] += 1

        if int(actual) == int(predicted):
            correct[int(actual)] += 1

print("\nPer-class test accuracy:")

for index, name in enumerate(CLASS_NAMES):
    if total[index] == 0:
        print(f"{name}: NO TEST IMAGES")
    else:
        accuracy = correct[index] / total[index] * 100
        print(
            f"{name}: {accuracy:.2f}% "
            f"({correct[index]}/{total[index]})"
        )

# ============================================================
# SAVE CLASS ORDER
# ============================================================

with open(OUTPUT_CLASSES, "w", encoding="utf-8") as file:
    json.dump(CLASS_NAMES, file, indent=2, ensure_ascii=False)

print("\n" + "=" * 65)
print("RETRAINING FINISHED")
print("=" * 65)
print("Candidate model:", OUTPUT_MODEL)
print("Candidate labels:", OUTPUT_CLASSES)
print("The original production model has not been overwritten.")
