
import os
import json
import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

TEST_DIR = os.path.join(
    PROJECT_DIR, "dataset", "SKIN", "test"
)

MODEL_PATH = os.path.join(
    PROJECT_DIR,
    "backend",
    "models",
    "skin_disease_finetuned.keras"
)

CLASS_NAMES_PATH = os.path.join(
    PROJECT_DIR,
    "backend",
    "models",
    "class_names.json"
)

REPORT_DIR = os.path.join(
    PROJECT_DIR, "backend", "models"
)

REPORT_PATH = os.path.join(
    REPORT_DIR, "classification_report.txt"
)

CONFUSION_PATH = os.path.join(
    REPORT_DIR, "confusion_matrix.csv"
)

# ============================================================
# SETTINGS
# ============================================================

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
SEED = 123

# ============================================================
# CHECK REQUIRED FILES
# ============================================================

for path in [TEST_DIR, MODEL_PATH, CLASS_NAMES_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"\nRequired file or folder not found:\n{path}"
        )

os.makedirs(REPORT_DIR, exist_ok=True)

# ============================================================
# LOAD CLASS NAMES
# ============================================================

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
    class_names = json.load(file)

if not isinstance(class_names, list) or not class_names:
    raise ValueError(
        "class_names.json must contain a non-empty JSON list."
    )

if len(class_names) != len(set(class_names)):
    raise ValueError(
        "Duplicate class names found in class_names.json."
    )

print("=" * 65)
print("SKINCARE AI - MODEL EVALUATION")
print("=" * 65)

print(f"\nModel: {os.path.basename(MODEL_PATH)}")
print(f"Number of classes: {len(class_names)}")
print(f"Test folder: {TEST_DIR}")

# ============================================================
# LOAD TEST DATA
# ============================================================

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False,
    label_mode="int"
)

dataset_class_names = test_ds.class_names

print("\nChecking class order...")

if dataset_class_names != class_names:
    print("\nERROR: Class order mismatch!")
    print("\nOrder in class_names.json:")
    for index, name in enumerate(class_names):
        print(f"{index}: {name}")

    print("\nOrder detected in test directory:")
    for index, name in enumerate(dataset_class_names):
        print(f"{index}: {name}")

    raise ValueError(
        "Test directory class order does not match class_names.json. "
        "Evaluation stopped to prevent misleading results."
    )

print("Class order matches the test directory.")

# Improve input pipeline performance without changing image values.
test_ds = test_ds.prefetch(tf.data.AUTOTUNE)

# ============================================================
# LOAD MODEL
# ============================================================

print("\nLoading model...")

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

if model.output_shape[-1] != len(class_names):
    raise ValueError(
        f"Model outputs {model.output_shape[-1]} classes, "
        f"but class_names.json contains {len(class_names)}."
    )

print("Model loaded successfully.")
print(f"Input shape: {model.input_shape}")
print(f"Output shape: {model.output_shape}")

# ============================================================
# COLLECT TRUE LABELS
# ============================================================

y_true = np.concatenate([
    labels.numpy()
    for _, labels in test_ds
])

print(f"\nTotal test images: {len(y_true)}")

# ============================================================
# PREDICTIONS
# ============================================================

print("\nPredicting test images...")

probabilities = model.predict(
    test_ds,
    verbose=1
)

if probabilities.ndim != 2:
    raise ValueError(
        f"Expected 2D class probabilities, got {probabilities.shape}"
    )

if probabilities.shape[1] != len(class_names):
    raise ValueError(
        "Prediction output count does not match the class names."
    )

if len(probabilities) != len(y_true):
    raise ValueError(
        "Prediction count does not match the number of test labels."
    )

y_pred = np.argmax(probabilities, axis=1)

# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(y_true, y_pred)

report = classification_report(
    y_true,
    y_pred,
    labels=list(range(len(class_names))),
    target_names=class_names,
    digits=4,
    zero_division=0
)

matrix = confusion_matrix(
    y_true,
    y_pred,
    labels=list(range(len(class_names)))
)

# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n" + "=" * 65)
print("EVALUATION RESULTS")
print("=" * 65)

print(f"Model: {os.path.basename(MODEL_PATH)}")
print(f"Test images: {len(y_true)}")
print(f"Test accuracy: {accuracy * 100:.2f}%")

print("\nClassification Report:")
print(report)

print("\nPer-class accuracy:")

for index, class_name in enumerate(class_names):
    class_mask = y_true == index
    class_total = int(np.sum(class_mask))

    if class_total:
        class_accuracy = float(
            np.mean(y_pred[class_mask] == y_true[class_mask])
        )
    else:
        class_accuracy = 0.0

    print(
        f"{class_name}: "
        f"{class_accuracy * 100:.2f}% "
        f"({class_total} images)"
    )

# ============================================================
# SAVE REPORT
# ============================================================

with open(REPORT_PATH, "w", encoding="utf-8") as file:
    file.write("SKINCARE AI - MODEL EVALUATION\n")
    file.write("=" * 65 + "\n")
    file.write(f"Model: {os.path.basename(MODEL_PATH)}\n")
    file.write(f"Test images: {len(y_true)}\n")
    file.write(f"Test accuracy: {accuracy * 100:.2f}%\n\n")
    file.write("Class order:\n")

    for index, name in enumerate(class_names):
        file.write(f"{index}: {name}\n")

    file.write("\nClassification Report:\n")
    file.write(report)
    file.write("\n\nConfusion Matrix:\n")
    file.write(str(matrix))

np.savetxt(
    CONFUSION_PATH,
    matrix,
    delimiter=",",
    fmt="%d"
)

print("\n" + "=" * 65)
print("EVALUATION COMPLETED")
print("=" * 65)
print(f"Report saved to: {REPORT_PATH}")
print(f"Confusion matrix saved to: {CONFUSION_PATH}")
