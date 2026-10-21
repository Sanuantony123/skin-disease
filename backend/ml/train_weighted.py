
import os
import json
import numpy as np
import tensorflow as tf

from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report

# ============================================================
# PATHS AND SETTINGS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

TRAIN_DIR = os.path.join(BASE_DIR, "dataset", "SKIN", "train")
TEST_DIR = os.path.join(BASE_DIR, "dataset", "SKIN", "test")
MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")

SOURCE_MODEL = os.path.join(
    MODEL_DIR, "skin_disease_finetuned.keras"
)
CLASS_NAMES_PATH = os.path.join(
    MODEL_DIR, "class_names.json"
)
OUTPUT_MODEL = os.path.join(
    MODEL_DIR, "skin_disease_weighted.keras"
)
REPORT_PATH = os.path.join(
    MODEL_DIR, "weighted_classification_report.txt"
)

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
SEED = 123
EPOCHS = 5
NUM_CLASSES = 23

tf.keras.utils.set_random_seed(SEED)

# ============================================================
# VERIFY FILES AND CLASS ORDER
# ============================================================

for path in [TRAIN_DIR, TEST_DIR, SOURCE_MODEL, CLASS_NAMES_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing path: {path}")

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)

train_classes = sorted([
    d for d in os.listdir(TRAIN_DIR)
    if os.path.isdir(os.path.join(TRAIN_DIR, d))
])
test_classes = sorted([
    d for d in os.listdir(TEST_DIR)
    if os.path.isdir(os.path.join(TEST_DIR, d))
])

if class_names != train_classes or class_names != test_classes:
    raise ValueError(
        "Class order mismatch. Stop training and verify class_names.json."
    )

if len(class_names) != NUM_CLASSES:
    raise ValueError(f"Expected {NUM_CLASSES} classes.")

print("Classes verified:", len(class_names))

# ============================================================
# LOAD TRAINING AND VALIDATION DATA
# ============================================================

train_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    class_names=class_names,
    label_mode="int",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.20,
    subset="training",
    seed=SEED,
    shuffle=True
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    TRAIN_DIR,
    class_names=class_names,
    label_mode="int",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    validation_split=0.20,
    subset="validation",
    seed=SEED,
    shuffle=False
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    class_names=class_names,
    label_mode="int",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

# ============================================================
# CALCULATE CLASS WEIGHTS FROM TRAINING DATA ONLY
# ============================================================

print("\nCalculating class weights...")

counts = np.zeros(NUM_CLASSES, dtype=np.int64)

for _, labels in train_ds:
    counts += np.bincount(
        labels.numpy(),
        minlength=NUM_CLASSES
    )

if np.any(counts == 0):
    raise ValueError("At least one training class has no images.")

weights = compute_class_weight(
    class_weight="balanced",
    classes=np.arange(NUM_CLASSES),
    y=np.repeat(
        np.arange(NUM_CLASSES),
        counts
    )
)

class_weights = {
    i: float(weights[i])
    for i in range(NUM_CLASSES)
}

for i, name in enumerate(class_names):
    print(
        f"{name}: {counts[i]} training images, "
        f"weight={class_weights[i]:.3f}"
    )

# ============================================================
# PREPARE DATASETS
# ============================================================

train_ds = train_ds.prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.prefetch(tf.data.AUTOTUNE)
test_ds = test_ds.prefetch(tf.data.AUTOTUNE)

# ============================================================
# LOAD EXISTING BEST MODEL
# ============================================================

print("\nLoading existing model...")

model = tf.keras.models.load_model(
    SOURCE_MODEL,
    compile=False
)

if model.output_shape[-1] != NUM_CLASSES:
    raise ValueError("Model output count does not match class count.")

# Freeze early MobileNetV2 layers; fine-tune later layers.
base_model = model.get_layer("mobilenetv2_base")
base_model.trainable = True

for layer in base_model.layers[:-30]:
    layer.trainable = False

for layer in base_model.layers:
    if isinstance(layer, tf.keras.layers.BatchNormalization):
        layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ============================================================
# TRAIN WITH CLASS WEIGHTS
# ============================================================

callbacks = [
    tf.keras.callbacks.ModelCheckpoint(
        OUTPUT_MODEL,
        monitor="val_loss",
        mode="min",
        save_best_only=True,
        verbose=1
    ),
    tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        mode="min",
        patience=2,
        restore_best_weights=True,
        verbose=1
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.3,
        patience=1,
        min_lr=1e-7,
        verbose=1
    )
]

print("\nStarting class-weighted fine-tuning...")

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=callbacks
)

# ============================================================
# EVALUATE EXPERIMENTAL MODEL
# ============================================================

print("\nLoading best weighted checkpoint...")

model = tf.keras.models.load_model(
    OUTPUT_MODEL,
    compile=False
)

print("\nEvaluating on test dataset...")

loss, accuracy = model.evaluate(test_ds, verbose=1)

y_true = np.concatenate([
    labels.numpy() for _, labels in test_ds
])

probabilities = model.predict(test_ds, verbose=1)
y_pred = np.argmax(probabilities, axis=1)

report = classification_report(
    y_true,
    y_pred,
    labels=list(range(NUM_CLASSES)),
    target_names=class_names,
    digits=4,
    zero_division=0
)

print(f"\nWeighted model test loss: {loss:.4f}")
print(f"Weighted model test accuracy: {accuracy * 100:.2f}%")
print("\nClassification report:\n")
print(report)

with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write(f"Test loss: {loss:.4f}\n")
    f.write(f"Test accuracy: {accuracy * 100:.2f}%\n\n")
    f.write(report)

print("\nExperimental model saved to:")
print(OUTPUT_MODEL)
print("\nReport saved to:")
print(REPORT_PATH)
print("\nOriginal model was not overwritten.")
