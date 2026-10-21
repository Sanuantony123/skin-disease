# -*- coding: utf-8 -*-
"""
Report Data Module for Skin Disease Prediction Documentation
Contains all text, tables, evaluation metrics, and clinical recommendations.
"""

PROJECT_TITLE = "SKIN DISEASE PREDICTION"
FULL_PROJECT_TITLE = "SKIN DISEASE PREDICTION AND HEALTHCARE RECOMMENDATION SYSTEM USING DEEP LEARNING"
COLLEGE_NAME = "MAR BASELIOS INSTITUTE OF TECHNOLOGY AND SCIENCE"
COLLEGE_LOCATION = "Nellimattom, Kothamangalam"
UNIVERSITY_AFFILIATION = "(Affiliated to APJ Abdul Kalam Technological University, TVM)"
DEPARTMENT_NAME = "Department of Computer Applications"
DEGREE_NAME = "Master of Computer Applications"
ACADEMIC_YEAR = "2025-2027"

STUDENT_NAME = "Name"
REG_NO = "---------"
GUIDE_NAME = "Prof. ---------"
HOD_NAME = "Prof. ---------"
COORDINATOR_NAME = "Prof. ---------"
EXAMINER_NAME = "Prof. ---------"

# 23 Disease Categories and Counts from Dataset
CLASSES_DATA = [
    ("Acne and Rosacea Photos", 840, 312, 1152),
    ("Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions", 1149, 288, 1437),
    ("Atopic Dermatitis Photos", 489, 123, 612),
    ("Bullous Disease Photos", 448, 113, 561),
    ("Cellulitis Impetigo and other Bacterial Infections", 288, 73, 361),
    ("Eczema Photos", 1235, 309, 1544),
    ("Exanthems and Drug Eruptions", 404, 101, 505),
    ("Hair Loss Photos Alopecia and other Hair Diseases", 239, 60, 299),
    ("Herpes HPV and other STDs Photos", 405, 102, 507),
    ("Light Diseases and Disorders of Pigmentation", 568, 143, 711),
    ("Lupus and other Connective Tissue diseases", 420, 105, 525),
    ("Melanoma Skin Cancer Nevi and Moles", 463, 116, 579),
    ("Nail Fungus and other Nail Disease", 1040, 261, 1301),
    ("Poison Ivy Photos and other Contact Dermatitis", 260, 65, 325),
    ("Psoriasis pictures Lichen Planus and related diseases", 1405, 352, 1757),
    ("Scabies Lyme Disease and other Infestations and Bites", 431, 108, 539),
    ("Seborrheic Keratoses and other Benign Tumors", 1371, 343, 1714),
    ("Systemic Disease", 606, 152, 758),
    ("Tinea Ringworm Candidiasis and other Fungal Infections", 1300, 325, 1625),
    ("Urticaria Hives", 212, 53, 265),
    ("Vascular Tumors", 482, 121, 603),
    ("Vasculitis Photos", 416, 105, 521),
    ("Warts Molluscum and other Viral Infections", 1086, 272, 1358),
]

TOTAL_TRAIN_IMAGES = sum(c[1] for c in CLASSES_DATA)
TOTAL_TEST_IMAGES = sum(c[2] for c in CLASSES_DATA)
TOTAL_DATASET_IMAGES = sum(c[3] for c in CLASSES_DATA)

# Literature Review Papers
LITERATURE_PAPERS = [
    {
        "citation": "Esteva, A., Kuprel, B., Novoa, R. A., Ko, J., Swetter, S. M., Blau, H. M., & Thrun, S. (2017). Dermatologist-level classification of skin lesions with deep neural networks. Nature, 542(7639), 115-118.",
        "summary": "Demonstrated that deep convolutional neural networks (Inception v3) trained on a large dataset of 129,450 clinical dermatological images achieved diagnostic performance on par with 21 board-certified dermatologists across two critical clinical use cases: keratinocyte carcinomas versus benign seborrheic keratoses, and malignant melanomas versus benign nevi.",
        "strengths": "Pioneering clinical benchmark showing superhuman or parity-level CNN classification capability across major dermatological categories.",
        "limitations": "Model relied on massive compute resources and heavy architecture unsuitable for real-time mobile/edge deployment; lacked non-skin image rejection."
    },
    {
        "citation": "Sandler, M., Howard, A., Zhu, M., Zhmoginov, A., & Chen, L. C. (2018). MobileNetV2: Inverted Residuals and Linear Bottlenecks. Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 4510-4520.",
        "summary": "Introduced the MobileNetV2 architecture featuring inverted residual blocks where shortcut connections are placed between thin bottleneck layers and depthwise separable convolutions that decouple spatial filtering from channel-wise feature combination, slashing floating-point operations by up to 80% while retaining high feature representation fidelity.",
        "strengths": "High computational efficiency, lightweight parameter footprint (~3.5M parameters), excellent performance for real-time edge and web deployment.",
        "limitations": "Requires careful learning rate scheduling and progressive fine-tuning to prevent representational collapse when fine-tuning on fine-grained medical tasks."
    },
    {
        "citation": "Tschandl, P., Rosendahl, C., & Kittler, H. (2018). The HAM10000 dataset, a large collection of multi-source dermatological images of common pigmented skin lesions. Scientific Data, 5, 180161.",
        "summary": "Curated an open-access benchmark of 10,015 dermatoscopic images covering 7 common diagnostic categories. The study emphasized the necessity of data augmentation and class imbalance mitigation strategies in dermatological machine learning.",
        "strengths": "High-quality dermatoscopic images with histopathological verification across major pigmentary lesion classes.",
        "limitations": "Limited to pigmented lesions (7 classes) and does not cover common inflammatory, viral, bacterial, or fungal skin conditions (e.g., acne, eczema, ringworm, psoriasis)."
    },
    {
        "citation": "Ahmed, Khaled R. (2021). Smart Pothole Detection and Image Processing Using Deep Learning Based on Dilated Convolution. Sensors, 21(24), 8406.",
        "summary": "Evaluated transfer learning architectures (ResNet50, MobileNetV2, InceptionV3, and YOLO) for automated visual feature classification. Demonstrated that pre-trained ImageNet feature representations yield superior accuracy and convergence compared to randomly initialized deep networks.",
        "strengths": "Rigorous comparative framework demonstrating the efficacy of transfer learning and fine-tuning across distinct image classification tasks.",
        "limitations": "Did not explore multi-class fine-grained dermatological classification or pre-inference domain filtering."
    }
]

# Classification Report Data on 4,002 Test Images
CLASSIFICATION_RESULTS = [
    ("Acne and Rosacea Photos", "0.4450", "0.5833", "0.5049", 312),
    ("Actinic Keratosis Basal Cell Carcinoma", "0.4021", "0.3993", "0.4007", 288),
    ("Atopic Dermatitis Photos", "0.2619", "0.2683", "0.2651", 123),
    ("Bullous Disease Photos", "0.2857", "0.0531", "0.0896", 113),
    ("Cellulitis Impetigo & Bacterial Infections", "0.1520", "0.1233", "0.1362", 73),
    ("Eczema Photos", "0.2851", "0.4078", "0.3356", 309),
    ("Exanthems and Drug Eruptions", "0.3012", "0.2475", "0.2717", 101),
    ("Hair Loss Photos Alopecia", "0.3065", "0.6333", "0.4130", 60),
    ("Herpes HPV and other STDs Photos", "0.4737", "0.0882", "0.1488", 102),
    ("Light Diseases & Pigmentation Disorders", "0.2368", "0.1259", "0.1644", 143),
    ("Lupus & Connective Tissue diseases", "0.1579", "0.0571", "0.0839", 105),
    ("Melanoma Skin Cancer Nevi & Moles", "0.3399", "0.4483", "0.3866", 116),
    ("Nail Fungus and other Nail Disease", "0.6871", "0.7739", "0.7279", 261),
    ("Poison Ivy & Contact Dermatitis", "0.1840", "0.1538", "0.1675", 65),
    ("Psoriasis pictures Lichen Planus", "0.2233", "0.3807", "0.2815", 352),
    ("Scabies Lyme Disease & Bites", "0.4231", "0.1019", "0.1642", 108),
    ("Seborrheic Keratoses & Benign Tumors", "0.3395", "0.4781", "0.3971", 343),
    ("Systemic Disease", "0.1974", "0.0987", "0.1316", 152),
    ("Tinea Ringworm Candidiasis", "0.3585", "0.2923", "0.3220", 325),
    ("Urticaria Hives", "0.1888", "0.2075", "0.1977", 53),
    ("Vascular Tumors", "0.7143", "0.0413", "0.0781", 121),
    ("Vasculitis Photos", "0.3084", "0.3143", "0.3113", 105),
    ("Warts Molluscum & Viral Infections", "0.3228", "0.4118", "0.3619", 272),
]

# Layer Dimension Table for MobileNetV2 Architecture
LAYER_DIMENSIONS = [
    ("Input Layer", "(None, 224, 224, 3)", "Input image tensor (RGB)"),
    ("Data Augmentation", "(None, 224, 224, 3)", "RandomFlip, Rotation, Zoom, Contrast"),
    ("Rescaling", "(None, 224, 224, 3)", "Normalizes [0, 255] to [-1, 1] range"),
    ("Conv2D (Initial)", "(None, 112, 112, 32)", "3x3 Conv, Stride 2, ReLU6"),
    ("Bottleneck 1", "(None, 112, 112, 16)", "Inverted Residual Block (t=1, c=16, s=1)"),
    ("Bottleneck 2-3", "(None, 56, 56, 24)", "2 Inverted Residual Blocks (t=6, c=24, s=2)"),
    ("Bottleneck 4-6", "(None, 28, 28, 32)", "3 Inverted Residual Blocks (t=6, c=32, s=2)"),
    ("Bottleneck 7-10", "(None, 14, 14, 64)", "4 Inverted Residual Blocks (t=6, c=64, s=2)"),
    ("Bottleneck 11-13", "(None, 14, 14, 96)", "3 Inverted Residual Blocks (t=6, c=96, s=1)"),
    ("Bottleneck 14-16", "(None, 7, 7, 160)", "3 Inverted Residual Blocks (t=6, c=160, s=2)"),
    ("Bottleneck 17", "(None, 7, 7, 320)", "1 Inverted Residual Block (t=6, c=320, s=1)"),
    ("1x1 Conv2D", "(None, 7, 7, 1280)", "1x1 Conv feature expansion + ReLU6"),
    ("GlobalAveragePooling2D", "(None, 1280)", "Spatial dimension reduction to 1D vector"),
    ("Dropout (0.35)", "(None, 1280)", "Regularization to prevent overfitting"),
    ("Dense (Output)", "(None, 23)", "Fully connected layer with Softmax activation"),
]
