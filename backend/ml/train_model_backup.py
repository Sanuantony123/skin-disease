
import os
import json
import shutil
import numpy as np
import tensorflow as tf

from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import (
    EarlyStopping,
    ModelCheckpoint,
    ReduceLROnPlateau
)
from sklearn.metrics import classification_report


# ============================================================
# 1. SETTINGS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

TRAIN_DIR = os.path.join(BASE_DIR, "dataset", "SKIN", "train")
TEST_DIR = os.path.join(BASE_DIR, "dataset", "SKIN", "test")

MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")

MODEL_PATH = os.path.join(
    MODEL_DIR, "skin_disease_model.keras"
)

CLASS_NAMES_PATH = os.path.join(
    MODEL_DIR, "class_names.json"
)

STAGE1_PATH = os.path.join(
    MODEL_DIR, "skin_disease_stage1.keras"
)

STAGE2_PATH = os.path.join(
    MODEL_DIR, "skin_disease_finetuned.keras"
)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 123
VALIDATION_SPLIT = 0.20

STAGE1_EPOCHS = 10
STAGE2_EPOCHS = 15
NUM_CLASSES = 23

tf.keras.utils.set_random_seed(SEED)
os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# 2. CHECK DATASET
# ============================================================

print("=" * 70)
print("SKINCARE AI - SKIN DISEASE MODEL TRAINING")
print("=" * 70)

print("Project:", BASE_DIR)
print("Training data:", TRAIN_DIR)
print("Testing data:", TEST_DIR)

if not os.path.isdir(TRAIN_DIR):
    raise FileNotFoundError(
        f"Training directory not found: {TRAIN_DIR}"
    )

if not os.path.isdir(TEST_DIR):
    raise FileNotFoundError(
        f"Testing directory not found: {TEST_DIR}"
    )


# ============================================================
# 3. CHECK CLASS NAMES
# ============================================================

class_names = sorted([
    name
    for name in os.listdir(TRAIN_DIR)
    if os.path.isdir(os.path.join(TRAIN_DIR, name))
])

test_class_names = sorted([
    name
    for name in os.listdir(TEST_DIR)
    if os.path.isdir(os.path.join(TEST_DIR, name))
])

print("\nClasses found:", len(class_names))

for index, name in enumerate(class_names):
    print(f"{index}: {name}")

if len(class_names) != NUM_CLASSES:
    raise ValueError(
        f"Expected {NUM_CLASSES} training classes; "
        f"found {len(class_names)}."
    )

if class_names != test_class_names:
    raise ValueError(
        "Training and testing class folders do not match.\n"
        f"Training classes: {class_names}\n"
        f"Testing classes: {test_class_names}"
    )

with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as file:
    json.dump(class_names, file, indent=4, ensure_ascii=False)


# ============================================================
# 4. LOAD TRAINING DATA
# ============================================================

print("\nLoading training data...")

train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    labels="inferred",
    label_mode="int",
    class_names=class_names,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=VALIDATION_SPLIT,
    subset="training",
    seed=SEED,
    shuffle=True
)


# ============================================================
# 5. LOAD VALIDATION DATA
# ============================================================

print("\nLoading validation data...")

val_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    labels="inferred",
    label_mode="int",
    class_names=class_names,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=VALIDATION_SPLIT,
    subset="validation",
    seed=SEED,
    shuffle=False
)


# ============================================================
# 6. LOAD TEST DATA
# ============================================================

print("\nLoading test data...")

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    labels="inferred",
    label_mode="int",
    class_names=class_names,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)


# ============================================================
# 7. DATA AUGMENTATION
# ============================================================

data_augmentation = tf.keras.Sequential(
    [
        layers.RandomFlip("horizontal"),
        layers.RandomRotation(0.08),
        layers.RandomZoom(0.10),
        layers.RandomContrast(0.10),
    ],
    name="data_augmentation"
)


# ============================================================
# 8. PREPARE DATASETS
# ============================================================

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)
test_ds = test_ds.prefetch(AUTOTUNE)


# ============================================================
# 9. BUILD MODEL
# ============================================================

print("\nBuilding MobileNetV2 model...")

base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet",
    name="mobilenetv2_base"
)

# Stage 1: freeze pretrained layers
base_model.trainable = False

inputs = layers.Input(
    shape=(224, 224, 3),
    name="image"
)

x = data_augmentation(inputs)

# Scale image values from [0, 255] to [-1, 1].
# This avoids the previous Lambda serialization error.
x = layers.Rescaling(
    scale=1.0 / 127.5,
    offset=-1.0,
    name="mobilenet_preprocessing"
)(x)

# Keep BatchNormalization in inference mode
x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.35)(x)

outputs = layers.Dense(
    NUM_CLASSES,
    activation="softmax",
    name="predictions"
)(x)

model = models.Model(
    inputs=inputs,
    outputs=outputs,
    name="SkinCareAI_MobileNetV2"
)


# ============================================================
# 10. CALLBACK FACTORY
# ============================================================

def create_callbacks(checkpoint_path):
    return [
        ModelCheckpoint(
            filepath=checkpoint_path,
            monitor="val_loss",
            mode="min",
            save_best_only=True,
            verbose=1
        ),
        EarlyStopping(
            monitor="val_loss",
            mode="min",
            patience=4,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor="val_loss",
            factor=0.3,
            patience=2,
            min_lr=1e-7,
            verbose=1
        )
    ]


# ============================================================
# 11. STAGE 1: TRAIN CLASSIFICATION HEAD
# ============================================================

print("\n" + "=" * 70)
print("STAGE 1: TRAINING CLASSIFICATION HEAD")
print("=" * 70)

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.0001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

history_stage1 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=STAGE1_EPOCHS,
    callbacks=create_callbacks(STAGE1_PATH)
)

best_stage1_loss = min(
    history_stage1.history["val_loss"]
)

print("\nBest Stage 1 validation loss:", best_stage1_loss)


# ============================================================
# 12. STAGE 2: FINE-TUNE LATER LAYERS
# ============================================================

print("\n" + "=" * 70)
print("STAGE 2: FINE-TUNING MOBILENETV2")
print("=" * 70)

# Restore the best Stage 1 checkpoint
model = tf.keras.models.load_model(
    STAGE1_PATH,
    compile=False
)

base_model = model.get_layer("mobilenetv2_base")
base_model.trainable = True

# Freeze earlier layers; train only the later layers
for layer in base_model.layers[:-30]:
    layer.trainable = False

# Keep BatchNormalization layers frozen
for layer in base_model.layers:
    if isinstance(layer, layers.BatchNormalization):
        layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.00001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history_stage2 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=STAGE2_EPOCHS,
    callbacks=create_callbacks(STAGE2_PATH)
)

best_stage2_loss = min(
    history_stage2.history["val_loss"]
)

print("\nBest Stage 2 validation loss:", best_stage2_loss)


# ============================================================
# 13. SELECT THE BEST CHECKPOINT
# ============================================================

print("\nSelecting the checkpoint with the lowest validation loss...")

if best_stage2_loss < best_stage1_loss:
    shutil.copy2(STAGE2_PATH, MODEL_PATH)
    selected_stage = "Stage 2: fine-tuned model"
else:
    shutil.copy2(STAGE1_PATH, MODEL_PATH)
    selected_stage = "Stage 1: classification-head model"

print("Selected:", selected_stage)
print("Final model:", MODEL_PATH)


# ============================================================
# 14. LOAD SELECTED MODEL
# ============================================================

print("\nLoading selected model...")

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.00001
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# ============================================================
# 15. EVALUATE ON UNSEEN TEST DATA
# ============================================================

print("\n" + "=" * 70)
print("FINAL TEST EVALUATION")
print("=" * 70)

test_loss, test_accuracy = model.evaluate(
    test_ds,
    verbose=1
)

print(f"\nTest loss: {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy * 100:.2f}%")


# ============================================================
# 16. PER-CLASS PERFORMANCE
# ============================================================

print("\nGenerating per-class performance report...")

y_true = np.concatenate([
    labels.numpy()
    for _, labels in test_ds
])

probabilities = model.predict(
    test_ds,
    verbose=1
)

y_pred = np.argmax(probabilities, axis=1)

report = classification_report(
    y_true,
    y_pred,
    labels=list(range(len(class_names))),
    target_names=class_names,
    zero_division=0,
    digits=4
)

print("\nPER-CLASS CLASSIFICATION REPORT")
print("=" * 70)
print(report)

report_path = os.path.join(
    MODEL_DIR,
    "classification_report.txt"
)

with open(report_path, "w", encoding="utf-8") as file:
    file.write(report)

print("\nClassification report saved to:")
print(report_path)


# ============================================================
# 17. FINAL INFORMATION
# ============================================================

print("\n" + "=" * 70)
print("TRAINING AND EVALUATION FINISHED")
print("=" * 70)

print("\nSelected model:")
print(MODEL_PATH)

print("\nClass names:")
print(CLASS_NAMES_PATH)

print("\nNumber of classes:", len(class_names))
print(f"Test accuracy: {test_accuracy * 100:.2f}%")
print(f"Test loss: {test_loss:.4f}")

print("\nDONE!")
