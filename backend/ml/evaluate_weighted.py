
import os
import json
import numpy as np
import tensorflow as tf

from sklearn.metrics import classification_report, confusion_matrix

# ============================================================
# PATHS AND SETTINGS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

TEST_DIR = os.path.join(BASE_DIR, "dataset", "SKIN", "test")
MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")

MODEL_PATH = os.path.join(
    MODEL_DIR, "skin_disease_weighted.keras"
)

CLASS_NAMES_PATH = os.path.join(
    MODEL_DIR, "class_names.json"
)

REPORT_PATH = os.path.join(
    MODEL_DIR, "weighted_classification_report.txt"
)

CONFUSION_PATH = os.path.join(
    MODEL_DIR, "weighted_confusion_matrix.csv"
)

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
NUM_CLASSES = 23

# ============================================================
# VERIFY REQUIRED FILES
# ============================================================

for path in [TEST_DIR, MODEL_PATH, CLASS_NAMES_PATH]:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Required file or folder not found:\n{path}"
        )

# ============================================================
# LOAD CLASS NAMES
# ============================================================

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
    class_names = json.load(file)

if len(class_names) != NUM_CLASSES:
    raise ValueError(
        f"Expected {NUM_CLASSES} classes, found {len(class_names)}."
    )

test_classes = sorted([
    folder
    for folder in os.listdir(TEST_DIR)
    if os.path.isdir(os.path.join(TEST_DIR, folder))
])

if class_names != test_classes:
    raise ValueError(
        "Class order mismatch between class_names.json and test folders."
    )

print("=" * 60)
print("WEIGHTED SKIN DISEASE MODEL EVALUATION")
print("=" * 60)
print("Number of classes:", len(class_names))

# ============================================================
# LOAD TEST DATA
# ============================================================

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    class_names=class_names,
    label_mode="int",
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_ds = test_ds.prefetch(tf.data.AUTOTUNE)

# ============================================================
# LOAD SAVED MODEL
# ============================================================

print("\nLoading saved weighted model...")

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False
)

if model.output_shape[-1] != NUM_CLASSES:
    raise ValueError(
        f"Model has {model.output_shape[-1]} outputs; "
        f"expected {NUM_CLASSES}."
    )

# Compile before using model.evaluate().
# Compilation does not retrain the model.
model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=1e-5
    ),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

# ============================================================
# EVALUATE MODEL
# ============================================================

print("\nEvaluating on test images...")

test_loss, test_accuracy = model.evaluate(
    test_ds,
    verbose=1
)

# ============================================================
# GENERATE PREDICTIONS
# ============================================================

print("\nGenerating predictions...")

y_true = np.concatenate([
    labels.numpy()
    for _, labels in test_ds
])

probabilities = model.predict(
    test_ds,
    verbose=1
)

y_pred = np.argmax(probabilities, axis=1)

if len(y_true) != len(y_pred):
    raise ValueError("Number of predictions does not match test labels.")

# ============================================================
# CLASSIFICATION REPORT
# ============================================================

report = classification_report(
    y_true,
    y_pred,
    labels=list(range(NUM_CLASSES)),
    target_names=class_names,
    digits=4,
    zero_division=0
)

print("\n" + "=" * 60)
print("FINAL TEST RESULTS")
print("=" * 60)

print(f"Test images: {len(y_true)}")
print(f"Test loss: {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy * 100:.2f}%")

print("\nCLASSIFICATION REPORT")
print("-" * 60)
print(report)

# ============================================================
# PER-CLASS ACCURACY
# ============================================================

matrix = confusion_matrix(
    y_true,
    y_pred,
    labels=list(range(NUM_CLASSES))
)

print("\nPER-CLASS ACCURACY")
print("-" * 60)

for i, name in enumerate(class_names):
    total = int(matrix[i].sum())
    correct = int(matrix[i, i])

    accuracy = (
        correct / total * 100
        if total > 0
        else 0.0
    )

    print(
        f"{i}: {name} -> "
        f"{correct}/{total} correct ({accuracy:.2f}%)"
    )

# ============================================================
# SAVE REPORT AND CONFUSION MATRIX
# ============================================================

with open(REPORT_PATH, "w", encoding="utf-8") as file:
    file.write("WEIGHTED SKIN DISEASE MODEL EVALUATION\n")
    file.write("=" * 60 + "\n")
    file.write(f"Test images: {len(y_true)}\n")
    file.write(f"Test loss: {test_loss:.4f}\n")
    file.write(
        f"Test accuracy: {test_accuracy * 100:.2f}%\n\n"
    )
    file.write("CLASSIFICATION REPORT\n")
    file.write(report)
    file.write("\n\nPER-CLASS ACCURACY\n")

    for i, name in enumerate(class_names):
        total = int(matrix[i].sum())
        correct = int(matrix[i, i])

        accuracy = (
            correct / total * 100
            if total > 0
            else 0.0
        )

        file.write(
            f"{i}: {name} -> "
            f"{correct}/{total} ({accuracy:.2f}%)\n"
        )

np.savetxt(
    CONFUSION_PATH,
    matrix,
    delimiter=",",
    fmt="%d"
)

print("\n" + "=" * 60)
print("EVALUATION COMPLETED")
print("=" * 60)
print("Report:", REPORT_PATH)
print("Confusion matrix:", CONFUSION_PATH)
print("The saved model was not retrained or overwritten.")
