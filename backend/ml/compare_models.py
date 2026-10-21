
import os
import tensorflow as tf

ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../..")
)

TEST_DIR = os.path.join(ROOT, "dataset", "SKIN", "test")
MODEL_DIR = os.path.join(ROOT, "backend", "models")

IMG_SIZE = (224, 224)
BATCH_SIZE = 16

test_ds = tf.keras.utils.image_dataset_from_directory(
    TEST_DIR,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=False
).prefetch(tf.data.AUTOTUNE)

model_files = [
    "skin_disease_stage1.keras",
    "skin_disease_finetuned.keras",
    "skin_disease_stage2_retrained.keras",
]

for filename in model_files:
    path = os.path.join(MODEL_DIR, filename)

    if not os.path.isfile(path):
        print(f"\nSkipping missing file: {filename}")
        continue

    print(f"\nEvaluating: {filename}")

    model = tf.keras.models.load_model(path)

    loss, accuracy = model.evaluate(test_ds, verbose=1)

    print(f"Model: {filename}")
    print(f"Test loss: {loss:.4f}")
    print(f"Test accuracy: {accuracy * 100:.2f}%")

    del model
