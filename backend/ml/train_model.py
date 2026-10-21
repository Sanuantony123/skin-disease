
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
from sklearn.metrics import classification_report, confusion_matrix


# ============================================================
# 1. SETTINGS
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)

TRAIN_DIR = os.path.join(BASE_DIR, "dataset", "SKIN", "train")
TEST_DIR = os.path.join(BASE_DIR, "dataset", "SKIN", "test")
MODEL_DIR = os.path.join(BASE_DIR, "backend", "models")

# Model path used by the application.
MODEL_PATH = os.path.join(
    MODEL_DIR, "skin_disease_model.keras"
)

CLASS_NAMES_PATH = os.path.join(
    MODEL_DIR, "class_names.json"
)

# Candidate checkpoint names protect the previous checkpoints.
STAGE1_PATH = os.path.join(
    MODEL_DIR, "skin_disease_stage1_candidate.keras"
)

STAGE2_PATH = os.path.join(
    MODEL_DIR, "skin_disease_finetuned_candidate.keras"
)

IMG_SIZE = (224, 224)
BATCH_SIZE = 32
SEED = 123
VALIDATION_SPLIT = 0.20
NUM_CLASSES = 23

STAGE1_EPOCHS = 10
STAGE2_EPOCHS = 15

AUTOTUNE = tf.data.AUTOTUNE

tf.keras.utils.set_random_seed(SEED)
os.makedirs(MODEL_DIR, exist_ok=True)


# ============================================================
# 2. CHECK DATASET DIRECTORIES
# ============================================================

print("=" * 70)
print("SKINCARE AI - MODEL TRAINING")
print("=" * 70)

print("Project directory:", BASE_DIR)
print("Training directory:", TRAIN_DIR)
print("Testing directory:", TEST_DIR)

if not os.path.isdir(TRAIN_DIR):
    raise FileNotFoundError(
        f"Training directory not found: {TRAIN_DIR}"
    )

if not os.path.isdir(TEST_DIR):
    raise FileNotFoundError(
        f"Testing directory not found: {TEST_DIR}"
    )


# ============================================================
# 3. VERIFY CLASS MAPPING
# ============================================================

class_names = sorted(
    name for name in os.listdir(TRAIN_DIR)
    if os.path.isdir(os.path.join(TRAIN_DIR, name))
)

test_class_names = sorted(
    name for name in os.listdir(TEST_DIR)
    if os.path.isdir(os.path.join(TEST_DIR, name))
)

if len(class_names) != NUM_CLASSES:
    raise ValueError(
        f"Expected {NUM_CLASSES} classes, "
        f"but found {len(class_names)}."
    )

if class_names != test_class_names:
    raise ValueError(
        "Training and testing class folders do not match."
    )

if os.path.exists(CLASS_NAMES_PATH):
    with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
        saved_class_names = json.load(file)

    if saved_class_names != class_names:
        raise ValueError(
            "Class mapping mismatch. Training stopped to protect "
            "the existing model labels.\n"
            f"Saved mapping: {saved_class_names}\n"
            f"Dataset mapping: {class_names}"
        )

    print("\nExisting class mapping verified.")
else:
    with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as file:
        json.dump(
            class_names,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nClass mapping created.")

print("Number of classes:", len(class_names))

for index, name in enumerate(class_names):
    print(f"{index}: {name}")


# ============================================================
# 4. LOAD DATASETS
# ============================================================

print("\nLoading training dataset...")

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

print("\nLoading validation dataset...")

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

print("\nLoading test dataset...")

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    labels="inferred",
    label_mode="int",
    class_names=class_names,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
)

train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)
test_ds = test_ds.prefetch(AUTOTUNE)

print("\nDataset loading completed.")


# ============================================================
# 5. DATA AUGMENTATION
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
# 6. BUILD MOBILE NET V2 MODEL
# ============================================================

def build_model():
    print("\nBuilding MobileNetV2...")

    base_model = MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights="imagenet",
        name="mobilenetv2_base"
    )

    base_model.trainable = False

    inputs = layers.Input(
        shape=(224, 224, 3),
        name="image"
    )

    x = data_augmentation(inputs)

    # MobileNetV2 preprocessing: [0, 255] -> [-1, 1].
    x = layers.Rescaling(
        scale=1.0 / 127.5,
        offset=-1.0,
        name="mobilenet_preprocessing"
    )(x)

    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.35)(x)

    outputs = layers.Dense(
        NUM_CLASSES,
        activation="softmax",
        name="predictions"
    )(x)

    return models.Model(
        inputs=inputs,
        outputs=outputs,
        name="SkinCareAI_MobileNetV2"
    )


# ============================================================
# 7. TRAINING CALLBACKS
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
            restore_best_weights=False,
            verbose=1
        ),

        ReduceLROnPlateau(
            monitor="val_loss",
            mode="min",
            factor=0.3,
            patience=2,
            min_lr=1e-7,
            verbose=1
        )
    ]


# ============================================================
# 8. COMPILE MODEL
# ============================================================

def compile_model(model, learning_rate):
    model.compile(
        optimizer=tf.keras.optimizers.Adam(
            learning_rate=learning_rate
        ),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )


# ============================================================
# 9. STAGE 1: TRAIN CLASSIFICATION HEAD
# ============================================================

print("\n" + "=" * 70)
print("STAGE 1: TRAIN CLASSIFICATION HEAD")
print("=" * 70)

model = build_model()
compile_model(model, 0.0001)

history_stage1 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=STAGE1_EPOCHS,
    callbacks=create_callbacks(STAGE1_PATH)
)

if not os.path.exists(STAGE1_PATH):
    raise RuntimeError(
        "Stage 1 did not produce a checkpoint. "
        "Check the training errors before continuing."
    )


# ============================================================
# 10. STAGE 2: FINE-TUNE LATER LAYERS
# ============================================================

print("\n" + "=" * 70)
print("STAGE 2: FINE-TUNE MOBILENETV2")
print("=" * 70)

model = tf.keras.models.load_model(
    STAGE1_PATH,
    compile=False
)

base_model = model.get_layer("mobilenetv2_base")
base_model.trainable = True

# Freeze earlier pretrained layers.
for layer in base_model.layers[:-30]:
    layer.trainable = False

# BatchNormalization layers remain frozen.
for layer in base_model.layers:
    if isinstance(layer, layers.BatchNormalization):
        layer.trainable = False

compile_model(model, 0.00001)

history_stage2 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=STAGE2_EPOCHS,
    callbacks=create_callbacks(STAGE2_PATH)
)

if not os.path.exists(STAGE2_PATH):
    raise RuntimeError(
        "Stage 2 did not produce a checkpoint. "
        "The existing application model has not been replaced."
    )


# ============================================================
# 11. COMPARE CANDIDATE CHECKPOINTS ON VALIDATION DATA
# ============================================================

print("\n" + "=" * 70)
print("COMPARE CANDIDATE CHECKPOINTS")
print("=" * 70)


def validation_loss_for_model(path):
    candidate = tf.keras.models.load_model(
        path,
        compile=False
    )

    if candidate.output_shape[-1] != NUM_CLASSES:
        raise ValueError(
            f"Unexpected output count in {path}"
        )

    compile_model(candidate, 0.00001)

    results = candidate.evaluate(
        val_ds,
        verbose=1,
        return_dict=True
    )

    loss = float(results["loss"])
    del candidate

    return loss


stage1_val_loss = validation_loss_for_model(STAGE1_PATH)
stage2_val_loss = validation_loss_for_model(STAGE2_PATH)

print(f"\nStage 1 validation loss: {stage1_val_loss:.4f}")
print(f"Stage 2 validation loss: {stage2_val_loss:.4f}")

if stage2_val_loss < stage1_val_loss:
    candidate_path = STAGE2_PATH
    candidate_name = "Stage 2 fine-tuned model"
else:
    candidate_path = STAGE1_PATH
    candidate_name = "Stage 1 classification-head model"

print("Best newly trained candidate:", candidate_name)


# ============================================================
# 12. COMPARE WITH THE EXISTING APPLICATION MODEL
# ============================================================

print("\nChecking the existing application model...")

replace_existing_model = not os.path.exists(MODEL_PATH)
existing_val_loss = None

if os.path.exists(MODEL_PATH):
    try:
        existing_val_loss = validation_loss_for_model(MODEL_PATH)

        print(
            "Existing model validation loss:",
            f"{existing_val_loss:.4f}"
        )

        if candidate_path and stage2_val_loss >= 0:
            candidate_val_loss = min(
                stage1_val_loss,
                stage2_val_loss
            )

            replace_existing_model = (
                candidate_val_loss < existing_val_loss
            )

    except Exception as error:
        print(
            "\nWARNING: Could not evaluate the existing model:",
            str(error)
        )
        print(
            "The existing model will be preserved for safety."
        )
        replace_existing_model = False

if replace_existing_model:
    shutil.copy2(candidate_path, MODEL_PATH)
    print("\nThe new candidate improved validation loss.")
    print("Updated application model:", MODEL_PATH)
else:
    print(
        "\nThe existing application model was preserved."
    )
    print(
        "The newly trained candidate remains available at:",
        candidate_path
    )


# ============================================================
# 13. LOAD THE MODEL THAT WILL BE EVALUATED
# ============================================================

if os.path.exists(MODEL_PATH):
    selected_model_path = MODEL_PATH
else:
    # No previous application model exists.
    selected_model_path = candidate_path
    shutil.copy2(candidate_path, MODEL_PATH)

print("\nModel selected for final evaluation:")
print(selected_model_path)

model = tf.keras.models.load_model(
    selected_model_path,
    compile=False
)

compile_model(model, 0.00001)


# ============================================================
# 14. FINAL TEST EVALUATION
# ============================================================

print("\n" + "=" * 70)
print("FINAL TEST EVALUATION")
print("=" * 70)

test_results = model.evaluate(
    test_ds,
    verbose=1,
    return_dict=True
)

test_loss = float(test_results["loss"])
test_accuracy = float(test_results["accuracy"])

print(f"\nTest loss: {test_loss:.4f}")
print(f"Test accuracy: {test_accuracy * 100:.2f}%")


# ============================================================
# 15. CLASSIFICATION REPORT AND CONFUSION MATRIX
# ============================================================

print("\nGenerating classification report...")

y_true = np.concatenate(
    [labels.numpy() for _, labels in test_ds]
)

probabilities = model.predict(
    test_ds,
    verbose=1
)

y_pred = np.argmax(probabilities, axis=1)

report = classification_report(
    y_true,
    y_pred,
    labels=list(range(NUM_CLASSES)),
    target_names=class_names,
    zero_division=0,
    digits=4
)

print("\nCLASSIFICATION REPORT")
print("=" * 70)
print(report)

report_path = os.path.join(
    MODEL_DIR,
    "classification_report.txt"
)

with open(report_path, "w", encoding="utf-8") as file:
    file.write(
        "SKINCARE AI - MODEL EVALUATION\n"
        f"Model: {selected_model_path}\n"
        f"Test images: {len(y_true)}\n"
        f"Test accuracy: {test_accuracy * 100:.2f}%\n\n"
    )
    file.write(report)

matrix = confusion_matrix(
    y_true,
    y_pred,
    labels=list(range(NUM_CLASSES))
)

matrix_path = os.path.join(
    MODEL_DIR,
    "confusion_matrix.csv"
)

np.savetxt(
    matrix_path,
    matrix,
    delimiter=",",
    fmt="%d"
)


# ============================================================
# 16. FINISHED
# ============================================================

print("\n" + "=" * 70)
print("TRAINING AND EVALUATION COMPLETED")
print("=" * 70)

print("Application model:", MODEL_PATH)
print("Class mapping:", CLASS_NAMES_PATH)
print("Classification report:", report_path)
print("Confusion matrix:", matrix_path)
print(f"Test accuracy: {test_accuracy * 100:.2f}%")
print(f"Test loss: {test_loss:.4f}")

print("\nDONE!")
