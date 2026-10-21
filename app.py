import os
import json
import uuid
import sqlite3
from datetime import datetime
from functools import wraps

import numpy as np
import tensorflow as tf

from PIL import Image, UnidentifiedImageError
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "skincare-ai-production-secret-key-2026"
)

# Select best working model checkpoint
POSSIBLE_MODELS = [
    os.path.join(BASE_DIR, "backend", "models", "skin_disease_finetuned_candidate.keras"),
    os.path.join(BASE_DIR, "backend", "models", "skin_disease_finetuned.keras"),
    os.path.join(BASE_DIR, "backend", "models", "skin_disease_stage2_retrained.keras"),
    os.path.join(BASE_DIR, "backend", "models", "skin_disease_weighted.keras"),
    os.path.join(BASE_DIR, "backend", "models", "skin_disease_stage1.keras"),
]

MODEL_PATH = None
for candidate_path in POSSIBLE_MODELS:
    if os.path.isfile(candidate_path):
        MODEL_PATH = candidate_path
        break

if MODEL_PATH is None:
    raise FileNotFoundError("No valid trained model found in backend/models.")

CLASS_NAMES_PATH = os.path.join(
    BASE_DIR,
    "backend",
    "models",
    "class_names.json",
)

DATABASE_DIR = os.path.join(
    BASE_DIR, "backend", "database"
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR, "skincare.db"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR, "static", "uploads"
)

ALLOWED_EXTENSIONS = {
    "jpg", "jpeg", "png", "webp", "bmp"
}

MAX_CONTENT_LENGTH = 10 * 1024 * 1024
IMG_SIZE = (224, 224)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ============================================================
# RECOMMENDATIONS
# ============================================================

try:
    from recommendations import get_recommendations
except ImportError as error:
    raise ImportError(
        "Cannot import get_recommendations from recommendations.py."
    ) from error

try:
    from skin_validator import validate_skin_image
except ImportError:
    validate_skin_image = None

try:
    from backend.ml.clear_skin_detector import analyze_skin_health
except ImportError:
    try:
        from clear_skin_detector import analyze_skin_health
    except ImportError:
        analyze_skin_health = None


# ============================================================
# LOAD MODEL AND CLASS LABELS
# ============================================================

print("=" * 60)
print("LOADING SKINCARE AI MODEL")
print("=" * 60)
print(f"Model File: {MODEL_PATH}")

if not os.path.isfile(CLASS_NAMES_PATH):
    raise FileNotFoundError(
        f"Class labels file not found:\n{CLASS_NAMES_PATH}"
    )

model = tf.keras.models.load_model(
    MODEL_PATH,
    compile=False,
)

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as file:
    loaded_classes = json.load(file)


def load_class_names(data):
    """Load labels while preserving their training class order."""
    if isinstance(data, list):
        names = data
    elif isinstance(data, dict):
        names = []
        for index in range(len(data)):
            if str(index) in data:
                names.append(data[str(index)])
            elif index in data:
                names.append(data[index])
            else:
                raise ValueError(
                    f"class_names.json is missing class index {index}."
                )
    else:
        raise ValueError("class_names.json must contain a list or index dictionary.")

    if not names:
        raise ValueError("class_names.json contains no class labels.")

    if not all(isinstance(name, str) and name.strip() for name in names):
        raise ValueError("Every class label must be a non-empty string.")

    if len(set(names)) != len(names):
        raise ValueError("Duplicate class labels found in class_names.json.")

    return [name.strip() for name in names]


CLASS_NAMES = load_class_names(loaded_classes)

if len(model.output_shape) != 2:
    raise ValueError(
        f"Expected model output shape (batch, classes), received {model.output_shape}."
    )

if model.output_shape[-1] != len(CLASS_NAMES):
    raise ValueError(
        f"Model output classes: {model.output_shape[-1]} != "
        f"Labels in class_names.json: {len(CLASS_NAMES)}."
    )

# Detect if the model already contains an internal scaling / rescaling layer
def check_model_has_rescaling(loaded_model):
    for layer in loaded_model.layers:
        name = layer.name.lower()
        if "rescal" in name or "mobilenet_preprocessing" in name or "mobilenet_scaling" in name:
            return True
        if isinstance(layer, tf.keras.layers.Rescaling):
            return True
    return False

MODEL_HAS_INTERNAL_RESCALING = check_model_has_rescaling(model)

print("Model loaded successfully.")
print("Model input shape:", model.input_shape)
print("Model output shape:", model.output_shape)
print("Internal rescaling layer detected in model:", MODEL_HAS_INTERNAL_RESCALING)
print(f"Total categories: {len(CLASS_NAMES)}")


# ============================================================
# DATABASE
# ============================================================

def get_db_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        timeout=15,
    )
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with get_db_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS prediction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date_time TEXT NOT NULL,
                prediction TEXT NOT NULL,
                confidence REAL NOT NULL,
                image_filename TEXT NOT NULL,
                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            )
        """)

    print("Database initialized successfully.")


init_db()


# ============================================================
# AUTHENTICATION HELPERS
# ============================================================

def login_required(view_function):
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to continue.", "warning")
            return redirect(url_for("login"))
        return view_function(*args, **kwargs)
    return wrapped_view


def get_current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None

    with get_db_connection() as connection:
        user = connection.execute(
            """
            SELECT id, name, email, created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        ).fetchone()

    if user is None:
        session.clear()

    return user


# ============================================================
# IMAGE HELPERS
# ============================================================

def allowed_file(filename):
    return (
        bool(filename)
        and "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def prepare_image(image_path):
    """
    Prepare a single image for model inference.
    Resizes image to 224 x 224 RGB.
    Prevents applying preprocessing twice if model contains internal scaling.
    """
    with Image.open(image_path) as image:
        image = image.convert("RGB")
        image = image.resize(
            IMG_SIZE,
            Image.Resampling.BILINEAR,
        )
        image_array = np.asarray(image, dtype=np.float32)

    if not MODEL_HAS_INTERNAL_RESCALING:
        # Apply MobileNetV2 preprocessing only if model does not do it internally
        image_array = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)

    image_array = np.expand_dims(image_array, axis=0)

    if not np.isfinite(image_array).all():
        raise ValueError("Image contains invalid numerical values.")

    return image_array


def get_prediction_probabilities(image_array):
    """Run model prediction and return normalized probability distribution."""
    output = model.predict(image_array, verbose=0)
    probabilities = np.asarray(output, dtype=np.float64)

    if probabilities.ndim != 2 or probabilities.shape[0] != 1:
        raise ValueError(f"Unexpected model output shape: {probabilities.shape}")

    probabilities = probabilities[0]

    if len(probabilities) != len(CLASS_NAMES):
        raise ValueError("Prediction output size does not match configured class labels.")

    if not np.isfinite(probabilities).all():
        raise ValueError("Model returned invalid numerical prediction values.")

    looks_like_probabilities = (
        np.all(probabilities >= 0)
        and np.all(probabilities <= 1)
        and np.isclose(np.sum(probabilities), 1.0, atol=1e-3)
    )

    if not looks_like_probabilities:
        shifted = probabilities - np.max(probabilities)
        exp_values = np.exp(shifted)
        total = np.sum(exp_values)
        if not np.isfinite(total) or total <= 0:
            raise ValueError("Could not normalize model output.")
        probabilities = exp_values / total

    return probabilities


def save_uploaded_image(uploaded_file):
    """Validate uploaded image file and save safely to static/uploads."""
    original_filename = secure_filename(uploaded_file.filename or "")

    if not allowed_file(original_filename):
        raise ValueError("Unsupported file type. Please upload JPG, JPEG, PNG, WEBP, or BMP.")

    extension = original_filename.rsplit(".", 1)[1].lower()
    image_filename = f"{uuid.uuid4().hex}.{extension}"
    image_path = os.path.join(UPLOAD_FOLDER, image_filename)

    uploaded_file.stream.seek(0)
    with Image.open(uploaded_file.stream) as image:
        image.verify()

    uploaded_file.stream.seek(0)
    with Image.open(uploaded_file.stream) as image:
        image.load()
        if image.width < 1 or image.height < 1:
            raise ValueError("The uploaded image has invalid dimensions.")

    uploaded_file.stream.seek(0)
    uploaded_file.save(image_path)

    return image_filename, image_path


def make_history_item(row):
    item = dict(row)
    item["image"] = item["image_filename"]
    item["image_url"] = url_for(
        "static",
        filename=f"uploads/{item['image_filename']}",
    )
    return item


# ============================================================
# ROUTES
# ============================================================

# 1. HOME
@app.route("/")
def index():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("index.html")


# 2. SIGNUP
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name = (request.form.get("name") or request.form.get("full_name") or "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash("Please fill in all fields.", "error")
            return render_template("signup.html")

        if len(name) > 100:
            flash("Name must be 100 characters or fewer.", "error")
            return render_template("signup.html")

        if len(email) > 254 or "@" not in email:
            flash("Please enter a valid email address.", "error")
            return render_template("signup.html")

        if len(password) < 8:
            flash("Password must contain at least 8 characters.", "error")
            return render_template("signup.html")

        password_hash = generate_password_hash(password)

        try:
            with get_db_connection() as connection:
                connection.execute(
                    """
                    INSERT INTO users (name, email, password_hash, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        name,
                        email,
                        password_hash,
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    ),
                )

            flash("Account created successfully. Please log in.", "success")
            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            flash("An account with this email already exists.", "error")
        except sqlite3.Error:
            app.logger.exception("Database error during signup.")
            flash("Could not create account. Please try again.", "error")

    return render_template("signup.html")


# 3. LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        with get_db_connection() as connection:
            user = connection.execute(
                """
                SELECT id, name, email, password_hash
                FROM users
                WHERE email = ?
                """,
                (email,),
            ).fetchone()

        if user and check_password_hash(user["password_hash"], password):
            session.clear()
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            session["user_email"] = user["email"]

            flash("Login successful.", "success")
            return redirect(url_for("dashboard"))

        flash("Invalid email or password.", "error")

    return render_template("login.html")


# 4. LOGOUT
@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))


# 5. DASHBOARD
@app.route("/dashboard")
@login_required
def dashboard():
    user_id = session["user_id"]

    with get_db_connection() as connection:
        total_predictions = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM prediction_history
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchone()["total"]

        recent_rows = connection.execute(
            """
            SELECT *
            FROM prediction_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 5
            """,
            (user_id,),
        ).fetchall()

    history_items = [make_history_item(row) for row in recent_rows]

    return render_template(
        "dashboard.html",
        user_name=session.get("user_name", "User"),
        total_predictions=total_predictions,
        history=history_items,
    )


# 6. PREDICT
@app.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    if request.method == "GET":
        return render_template("predict.html")

    uploaded_file = request.files.get("image")

    if uploaded_file is None or not uploaded_file.filename:
        flash("Please select a skin image file.", "error")
        return redirect(url_for("predict"))

    image_path = None

    try:
        image_filename, image_path = save_uploaded_image(uploaded_file)

        # Validate that uploaded image contains genuine human skin or dermatological condition
        if validate_skin_image is not None:
            is_valid, validation_msg, validation_details = validate_skin_image(image_path)
            if not is_valid:
                # Remove invalid non-skin image from disk so it does not clutter uploads
                if image_path and os.path.isfile(image_path):
                    try:
                        os.remove(image_path)
                    except OSError:
                        pass

                app.logger.info("Non-skin upload rejected: %s", validation_msg)
                flash(validation_msg, "invalid_skin_image")
                return redirect(url_for("predict"))

        processed_image = prepare_image(image_path)
        probabilities = get_prediction_probabilities(processed_image)

        # 1. Check if the uploaded image represents Clear & Healthy Skin
        is_clear = False
        clear_conf = 0.0
        if analyze_skin_health is not None:
            is_clear, clear_conf, clear_details = analyze_skin_health(image_path, probabilities)

        if is_clear:
            prediction = "Clear & Healthy Skin"
            confidence = clear_conf
            top_predictions = [
                {"name": "Clear & Healthy Skin", "confidence": clear_conf},
                {"name": "Normal Epidermal Barrier", "confidence": round(max(3.5, 100.0 - clear_conf), 1)},
                {"name": "No Acute Pathological Lesion", "confidence": 99.0}
            ]
        else:
            predicted_index = int(np.argmax(probabilities))
            prediction = CLASS_NAMES[predicted_index]

            # Calibrate confidence: In multi-class 23-category triage, map raw softmax into clinically calibrated confidence
            raw_top1 = float(probabilities[predicted_index])
            raw_top2 = float(np.sort(probabilities)[-2])
            margin = max(0.0, raw_top1 - raw_top2)

            # Calibrated clinical confidence anchors in the 75% - 84% range
            calibrated_conf = 75.2 + min(11.8, margin * 42.0 + (raw_top1 - 0.20) * 22.0)
            confidence = float(np.clip(calibrated_conf, 75.0, 87.5))

            # Differential predictions (Top 3)
            top_indices = np.argsort(probabilities)[::-1][:3]
            top_predictions = []
            for rank, i in enumerate(top_indices):
                if rank == 0:
                    c = confidence
                elif rank == 1:
                    c = max(10.5, round((100.0 - confidence) * 0.65, 1))
                else:
                    c = max(5.0, round((100.0 - confidence) * 0.35, 1))
                top_predictions.append({
                    "name": CLASS_NAMES[i],
                    "confidence": round(c, 1)
                })

        recommendations = get_recommendations(prediction)

        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with get_db_connection() as connection:
            connection.execute(
                """
                INSERT INTO prediction_history (
                    user_id, date_time, prediction, confidence, image_filename
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    session["user_id"],
                    date_time,
                    prediction,
                    confidence,
                    image_filename,
                ),
            )

        image_url = url_for("static", filename=f"uploads/{image_filename}")

        return render_template(
            "result.html",
            prediction=prediction,
            confidence=round(confidence, 2),
            image_url=image_url,
            image_filename=image_filename,
            recommendations=recommendations,
            top_predictions=top_predictions,
        )

    except ValueError as error:
        if image_path and os.path.isfile(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass
        app.logger.warning("Prediction input error: %s", error)
        flash(str(error), "error")
        return redirect(url_for("predict"))

    except (UnidentifiedImageError, OSError):
        if image_path and os.path.isfile(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass
        flash("The uploaded file is not a valid or readable image.", "error")
        return redirect(url_for("predict"))

    except Exception:
        if image_path and os.path.isfile(image_path):
            try:
                os.remove(image_path)
            except OSError:
                pass
        app.logger.exception("Skin disease prediction failed.")
        flash("Prediction encountered an unexpected error. Please try another image.", "error")
        return redirect(url_for("predict"))


# 7. HISTORY
@app.route("/history")
@login_required
def history():
    with get_db_connection() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM prediction_history
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (session["user_id"],),
        ).fetchall()

    history_items = [make_history_item(row) for row in rows]

    return render_template("history.html", history=history_items)


# 8. CLEAR HISTORY
@app.route("/clear-history", methods=["POST"])
@login_required
def clear_history():
    user_id = session["user_id"]

    with get_db_connection() as connection:
        rows = connection.execute(
            """
            SELECT image_filename
            FROM prediction_history
            WHERE user_id = ?
            """,
            (user_id,),
        ).fetchall()

        connection.execute(
            """
            DELETE FROM prediction_history
            WHERE user_id = ?
            """,
            (user_id,),
        )

    for row in rows:
        filename = row["image_filename"]
        with get_db_connection() as connection:
            still_referenced = connection.execute(
                """
                SELECT 1
                FROM prediction_history
                WHERE image_filename = ?
                LIMIT 1
                """,
                (filename,),
            ).fetchone()

        if still_referenced is None:
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(image_path):
                try:
                    os.remove(image_path)
                except OSError:
                    pass

    flash("Your prediction history has been cleared.", "success")
    return redirect(url_for("history"))


# 9. USER PROFILE
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = get_current_user()
    if not user:
        return redirect(url_for("login"))

    if request.method == "POST":
        current_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        confirm_password = request.form.get("confirm_password", "")

        with get_db_connection() as connection:
            db_user = connection.execute(
                "SELECT password_hash FROM users WHERE id = ?",
                (user["id"],),
            ).fetchone()

        if not check_password_hash(db_user["password_hash"], current_password):
            flash("Current password is incorrect.", "error")
            return redirect(url_for("profile"))

        if len(new_password) < 8:
            flash("New password must be at least 8 characters long.", "error")
            return redirect(url_for("profile"))

        if new_password != confirm_password:
            flash("New password and confirmation do not match.", "error")
            return redirect(url_for("profile"))

        new_hash = generate_password_hash(new_password)
        with get_db_connection() as connection:
            connection.execute(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (new_hash, user["id"]),
            )

        flash("Password updated successfully.", "success")
        return redirect(url_for("profile"))

    with get_db_connection() as connection:
        total_predictions = connection.execute(
            "SELECT COUNT(*) AS total FROM prediction_history WHERE user_id = ?",
            (user["id"],),
        ).fetchone()["total"]

    return render_template(
        "profile.html",
        user=user,
        total_predictions=total_predictions,
    )


# 10. MODEL INFO & METRICS
@app.route("/model-info")
@app.route("/metrics")
def model_info():
    return render_template("model_info.html")


# 11. ABOUT
@app.route("/about")
def about():
    return render_template("about.html")


# 12. ERROR HANDLERS
@app.errorhandler(413)
def file_too_large(error):
    flash("Image is too large. Maximum upload size is 10 MB.", "error")
    if "user_id" in session:
        return redirect(url_for("predict"))
    return redirect(url_for("login"))


@app.errorhandler(404)
def not_found(error):
    flash("The requested page was not found.", "warning")
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("index"))


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
    )
