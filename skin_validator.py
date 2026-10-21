"""
Skin Image Validator Module for SkinCare AI
--------------------------------------------
Validates uploaded images to ensure they contain genuine human skin or dermatological
conditions across the 23 clinical classes before running disease classification.

Catches non-skin images (cars, vehicles, animals, pets, electronics, furniture,
nature/landscapes, food, documents, drawings, blank images, or random noise)
and provides clear user feedback to upload a correct skin disease image.
"""

import os
import json
import threading
from typing import Tuple, Dict, Any
import numpy as np
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import (
    MobileNetV2,
    decode_predictions,
    preprocess_input,
)

# Lock for thread-safe model loading
_model_lock = threading.Lock()
_imagenet_model = None

# Words in ImageNet corresponding to definitive non-skin objects
NON_SKIN_WORDS = [
    # Animals & Pets
    'dog', 'terrier', 'retriever', 'hound', 'spaniel', 'shepherd', 'poodle', 'collie',
    'cat', 'tabby', 'lion', 'tiger', 'cheetah', 'leopard', 'bear', 'wolf', 'fox',
    'bird', 'eagle', 'owl', 'parrot', 'duck', 'goose', 'swan', 'hen', 'cock', 'ostrich',
    'fish', 'shark', 'ray', 'salmon', 'trout', 'whale', 'dolphin',
    'frog', 'toad', 'lizard', 'snake', 'turtle', 'crocodile', 'alligator',
    'horse', 'zebra', 'cow', 'ox', 'sheep', 'goat', 'elephant', 'camel', 'deer',
    'rabbit', 'hare', 'hamster', 'mouse', 'rat', 'squirrel',
    # Vehicles & Transportation
    'car', 'convertible', 'limousine', 'sports_car', 'pickup', 'truck', 'van',
    'bus', 'cab', 'taxi', 'jeep', 'ambulance', 'fire_engine', 'racer',
    'bicycle', 'bike', 'motorcycle', 'moped', 'scooter', 'tricycle', 'unicycle',
    'airplane', 'airliner', 'warplane', 'aircraft', 'balloon', 'airship',
    'boat', 'ship', 'canoe', 'kayak', 'submarine', 'yacht', 'speedboat', 'steamer',
    'train', 'locomotive', 'railway', 'streetcar', 'tram',
    # Electronics, Computers, Gadgets
    'laptop', 'notebook', 'desktop', 'monitor', 'screen', 'television', 'tv',
    'keyboard', 'mouse', 'touchpad', 'joystick', 'ipod', 'telephone', 'cellular',
    'phone', 'modem', 'router', 'camera', 'radio', 'microphone', 'loudspeaker',
    # Furniture, Household, Instruments
    'chair', 'sofa', 'couch', 'table', 'desk', 'bed', 'wardrobe', 'bookcase',
    'cabinet', 'refrigerator', 'microwave', 'oven', 'toaster', 'washer',
    'lamp', 'clock', 'vase', 'pillow', 'quilt', 'curtain', 'rug', 'carpet',
    'bottle', 'cup', 'mug', 'bowl', 'plate', 'pitcher', 'fork', 'spoon', 'knife',
    'guitar', 'violin', 'piano', 'drum', 'flute', 'trumpet', 'accordion',
    # Architecture, Outdoor, Scenery
    'building', 'house', 'church', 'castle', 'palace', 'monastery', 'mosque',
    'bridge', 'pier', 'dam', 'lighthouse', 'tower', 'fountain', 'barn',
    'mountain', 'alp', 'volcano', 'valley', 'cliff', 'promontory',
    'lake', 'lakeside', 'seashore', 'ocean', 'river', 'waterfall', 'coral_reef',
    'forest', 'tree', 'flower', 'daisy', 'sunflower', 'rose', 'plant', 'grass',
    # Food, Groceries & Produce
    'pizza', 'hamburger', 'cheeseburger', 'hotdog', 'sandwich', 'burrito',
    'pie', 'potpie', 'cake', 'ice_cream', 'bagel', 'pretzel', 'loaf', 'bread',
    'apple', 'banana', 'orange', 'lemon', 'strawberry', 'grape', 'pomegranate',
    'fig', 'pineapple', 'broccoli', 'cabbage', 'carrot', 'corn', 'cucumber',
    'mushroom', 'soup', 'pasta', 'grocery', 'grocery_store'
]

# Words that can legitimately be triggered by dermatological skin / mucosal / medical images
SKIN_EXEMPT_WORDS = [
    'band_aid', 'sunscreen', 'face_powder', 'lipstick', 'lotion', 'mask',
    'syringe', 'stethoscope', 'pill_bottle', 'tick', 'hog', 'pig',
    'hair_slide', 'wig', 'hair_spray', 'nipple', 'velvet', 'dough',
    'sponge', 'sea_anemone', 'sea_cucumber', 'piggy_bank', 'chimpanzee'
]


def get_imagenet_model():
    """Singleton getter for the pre-trained ImageNet MobileNetV2 model."""
    global _imagenet_model
    if _imagenet_model is None:
        with _model_lock:
            if _imagenet_model is None:
                _imagenet_model = MobileNetV2(weights="imagenet")
    return _imagenet_model


def analyze_skin_tones(image: Image.Image) -> Tuple[float, float]:
    """
    Computes human skin and dermatological lesion pixel coverage across
    Fitzpatrick skin phototypes I through VI, erythema (inflamed rash),
    hyperpigmented lesions, oral mucosa, and dermoscopy margins.

    Returns:
        (whole_image_skin_ratio, effective_skin_ratio)
    """
    rgb = np.asarray(image.convert("RGB"), dtype=np.float32)
    R, G, B = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

    # 1. Fitzpatrick Skin Phototypes I to VI (RGB and YCrCb bounds)
    rgb_skin = (
        (R > 50) & (G > 28) & (B > 15)
        & (R >= G) & (R >= B)
        & ((np.maximum(np.maximum(R, G), B) - np.minimum(np.minimum(R, G), B)) > 8)
    )

    Y = 0.299 * R + 0.587 * G + 0.114 * B
    Cr = (R - Y) * 0.713 + 128
    Cb = (B - Y) * 0.564 + 128
    ycrcb_skin = (Cr >= 126) & (Cr <= 185) & (Cb >= 70) & (Cb <= 140)

    # 2. Erythematous rashes (acne, cellulitis, dermatitis, hives, vasculitis)
    erythema = (R > 70) & (R > 1.15 * G) & (R > 1.15 * B)

    # 3. Melanin & hyperpigmented lesions (melanoma, moles, seborrheic keratoses)
    dark_lesion = (R > 20) & (R < 140) & (R >= G) & (G >= B) & ((R - B) > 5)

    # 4. Mucosal and oral lesions (lichen planus oral, lip herpes, etc.)
    mucosa = (R > 75) & (R > G) & (G > B * 0.5) & (R - B > 12)

    # Combined skin/lesion mask
    skin_mask = (rgb_skin & ycrcb_skin) | erythema | dark_lesion | mucosa
    skin_ratio = float(np.mean(skin_mask))

    # 5. Handle dark/dermoscopy black camera borders
    foreground = (R + G + B) > 45
    fg_ratio = float(np.mean(foreground))
    if 0.08 < fg_ratio < 0.88:
        fg_skin_ratio = float(np.mean(skin_mask[foreground]))
    else:
        fg_skin_ratio = skin_ratio

    effective_skin_ratio = max(skin_ratio, fg_skin_ratio)
    return skin_ratio, effective_skin_ratio


def validate_skin_image(image_path: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validates whether an image contains a genuine human skin or dermatological condition.

    Returns:
        (is_valid: bool, user_message: str, details: dict)
    """
    if not os.path.isfile(image_path):
        return False, "Image file not found.", {"error": "file_not_found"}

    try:
        with Image.open(image_path) as opened_image:
            img = opened_image.convert("RGB")
    except Exception as error:
        return False, "Could not read the uploaded image file.", {"error": str(error)}

    # 1. Quality & Blank / Solid Color Check
    gray = np.asarray(img.convert("L"), dtype=np.float32)
    std_contrast = float(np.std(gray))
    if std_contrast < 10.0:
        return False, (
            "The uploaded image is blank, solid color, or lacks sufficient visual contrast. "
            "Please upload a clear photograph of the affected skin area."
        ), {"contrast": std_contrast, "reason": "insufficient_contrast"}

    # 2. Random Pixel Noise Check
    rgb_arr = np.asarray(img, dtype=np.float32)
    adj_diff = float(np.mean(np.abs(np.diff(rgb_arr, axis=0))))
    if adj_diff > 38.0:
        return False, (
            "The uploaded image appears corrupted or contains random pixel static. "
            "Please upload a clear photograph of the skin condition."
        ), {"adj_diff": adj_diff, "reason": "random_noise"}

    # 3. Skin Tone & Lesion Analysis
    skin_ratio, effective_skin_ratio = analyze_skin_tones(img)

    # If skin pixel ratio is virtually zero (< 8%), definitely non-skin
    if effective_skin_ratio < 0.08:
        return False, (
            "No human skin or dermatological lesion was detected in this photo. "
            "Please upload a clear photo of the skin condition."
        ), {"skin_ratio": effective_skin_ratio, "reason": "low_skin_ratio"}

    # 4. Semantic Object Classification (ImageNet)
    model = get_imagenet_model()
    img_resized = img.resize((224, 224), Image.Resampling.BILINEAR)
    arr_in = preprocess_input(np.expand_dims(np.asarray(img_resized, dtype=np.float32), 0))
    preds = model.predict(arr_in, verbose=0)
    top_preds = decode_predictions(preds, top=5)[0]

    top1_name = top_preds[0][1].lower()
    top1_prob = float(top_preds[0][2])

    # Check for skin/medical compatible classes
    has_skin_exempt = any(
        any(exempt in t[1].lower() for exempt in SKIN_EXEMPT_WORDS)
        for t in top_preds[:3]
    )

    if not has_skin_exempt:
        is_top1_non_skin = any(kw in top1_name for kw in NON_SKIN_WORDS)

        # Dynamic confidence threshold:
        # High skin ratio (>40%) requires higher non-skin confidence (>=35%)
        # Lower skin ratio (8%-40%) requires moderate confidence (>=16%)
        if effective_skin_ratio >= 0.40:
            threshold = 0.35
            cum_threshold = 0.50
        else:
            threshold = 0.16
            cum_threshold = 0.35

        if is_top1_non_skin and top1_prob >= threshold:
            detected_object = top1_name.replace("_", " ").title()
            return False, (
                f"The image appears to show an object ({detected_object}) rather than a human skin condition. "
                "Please upload a clear, focused image of the affected skin area."
            ), {
                "detected_object": detected_object,
                "confidence": round(top1_prob * 100, 1),
                "skin_ratio": effective_skin_ratio,
                "reason": "non_skin_object"
            }

        # Check cumulative non-skin probability across top-5 predictions
        non_skin_sum = sum(
            float(t[2]) for t in top_preds
            if any(kw in t[1].lower() for kw in NON_SKIN_WORDS)
        )
        if non_skin_sum >= cum_threshold:
            detected_object = top_preds[0][1].replace("_", " ").title()
            return False, (
                f"The image contains non-skin content ({detected_object}). "
                "Please upload a clear clinical photograph of the skin condition."
            ), {
                "detected_object": detected_object,
                "cumulative_prob": round(non_skin_sum * 100, 1),
                "skin_ratio": effective_skin_ratio,
                "reason": "cumulative_non_skin"
            }

    return True, "Valid skin disease image.", {
        "skin_ratio": effective_skin_ratio,
        "status": "valid"
    }
