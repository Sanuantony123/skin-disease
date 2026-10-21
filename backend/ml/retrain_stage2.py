
import os
import json
import tensorflow as tf

from tensorflow.keras import layers
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau


# ============================================================
# PATHS AND SETTINGS
# ============================================================

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

TRAIN_DIR = os.path.join(PROJECT_DIR, "dataset", "SKIN", "train")
TEST_DIR = os.path.join(PROJECT_DIR, "dataset", "SKIN", "test")
MODEL_DIR = os.path.join(PROJECT_DIR, "backend", "models")

STAGE1_PATH = os.path.join(
    MODEL_DIR, "skin_disease_stage1.keras"
)

OUTPUT_PATH = os.path.join(
    MODEL_DIR, "skin_disease_stage2_retrained.keras"
)

CLASS_NAMES_PATH = os.path.join(
    MODEL_DIR, "class_names.json"
)

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 5
SEED = 123


# ============================================================
# CHECK FILES
# ============================================================

if not os.path.isfile(STAGE1_PATH):
    raise FileNotFoundError(
        f"Stage 1 model not found: {STAGE1_PATH}"
    )

if not os.path.isdir(TRAIN_DIR):
    raise FileNotFoundError(
        f"Training dataset not found: {TRAIN_DIR}"
    )

if not os.path.isdir(TEST_DIR):
    raise FileNotFoundError(
        f"Testing dataset not found: {TEST_DIR}"
    )

os.makedirs(MODEL_DIR, exist_ok=True)

print("Loading training dataset...")

train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    validation_split=0.20,
    subset="training",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    validation_split=0.20,
    subset="validation",
    seed=SEED,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    shuffle=False,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    label_mode="int"
)

class_names = train_ds.class_names

if len(class_names) != 23:
    raise ValueError(
        f"Expected 23 classes, found {len(class_names)}: "
        f"{class_names}"
    )

if val_ds.class_names != class_names:
    raise ValueError("Training and validation class orders differ.")

if test_ds.class_names != class_names:
    raise ValueError("Training and test class orders differ.")

print("Classes:", class_names)

with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as f:
    json.dump(class_names, f, indent=2)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)
test_ds = test_ds.prefetch(AUTOTUNE)


# ============================================================
# LOAD STAGE 1 MODEL
# ============================================================

print("\nLoading saved Stage 1 model...")

model = tf.keras.models.load_model(STAGE1_PATH)

if model.output_shape[-1] != len(class_names):
    raise ValueError(
        f"Model outputs {model.output_shape[-1]} classes, "
        f"but dataset has {len(class_names)}."
    )

base_model = model.get_layer("mobilenetv2_base")

print("Stage 1 model loaded.")
print("Input shape:", model.input_shape)
print("Output shape:", model.output_shape)


# ============================================================
# STAGE 2: FINE-TUNING ONLY
# ============================================================

print("\nPreparing Stage 2 fine-tuning...")

base_model.trainable = True

# Freeze earlier layers and BatchNormalization layers.
for layer in base_model.layers[:-10]:
    layer.trainable = False

for layer in base_model.layers[-10:]:
    if isinstance(layer, layers.BatchNormalization):
        layer.trainable = False
    else:
        layer.trainable = True

print(
    "Trainable base-model layers:",
    sum(layer.trainable for layer in base_model.layers)
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-5
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# ============================================================
# CALLBACKS
# ============================================================

callbacks = [
    ModelCheckpoint(
        OUTPUT_PATH,
        monitor="val_loss",
        save_best_only=True,
        verbose=1
    ),
    EarlyStopping(
        monitor="val_loss",
        patience=3,
        restore_best_weights=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.2,
        patience=2,
        min_lr=1e-7,
        verbose=1
    )
]


# ============================================================
# TRAIN STAGE 2 ONLY
# ============================================================

print("\nStarting Stage 2 fine-tuning...")

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=callbacks
)

# Save the final in-memory model as well.
model.save(OUTPUT_PATH)

print("\nEvaluating the fine-tuned model...")

test_loss, test_accuracy = model.evaluate(test_ds, verbose=1)

print(f"\nTest loss: {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy * 100:.2f}%")
print("Fine-tuned model saved to:")
print(OUTPUT_PATH)
