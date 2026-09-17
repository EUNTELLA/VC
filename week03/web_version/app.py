# Created: 2026-09-17 10:32:30
"""Flask backend for the handwritten digit recognizer (web version).

Serves the drawing page and a /predict endpoint that classifies a canvas
drawing using the same kind of scikit-learn model trained by
train_model.py.
"""

import base64
import io
import os

import joblib
import numpy as np
from flask import Flask, jsonify, render_template, request
from PIL import Image

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "digit_model.joblib")
# The model is trained on 28x28 MNIST images; the drawn digit is scaled
# to fit within this box, leaving a border, matching classic MNIST
# preprocessing.
MODEL_IMAGE_SIZE = 28
DIGIT_BOX_SIZE = 20

app = Flask(__name__)

if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"Model not found at {MODEL_PATH}. Run train_model.py first."
    )
model = joblib.load(MODEL_PATH)


def decode_canvas_image(data_url):
    # data_url looks like "data:image/png;base64,...."
    _header, encoded = data_url.split(",", 1)
    image_bytes = base64.b64decode(encoded)
    return Image.open(io.BytesIO(image_bytes)).convert("L")


def preprocess_image(image):
    # Crop to the bounding box of the drawn strokes (ignore empty margins).
    bbox = image.getbbox()
    if bbox is None:
        return np.zeros((1, MODEL_IMAGE_SIZE * MODEL_IMAGE_SIZE))
    cropped = image.crop(bbox)

    # Resize so the longest side fits DIGIT_BOX_SIZE, preserving aspect
    # ratio, then paste centered onto a blank 28x28 canvas. This mirrors
    # how MNIST digits are framed and greatly improves accuracy on
    # freehand mouse drawings compared to a plain full-canvas resize.
    width, height = cropped.size
    scale = DIGIT_BOX_SIZE / max(width, height)
    new_size = (max(1, round(width * scale)), max(1, round(height * scale)))
    resized = cropped.resize(new_size, Image.LANCZOS)

    centered = Image.new("L", (MODEL_IMAGE_SIZE, MODEL_IMAGE_SIZE), color=0)
    paste_x = (MODEL_IMAGE_SIZE - new_size[0]) // 2
    paste_y = (MODEL_IMAGE_SIZE - new_size[1]) // 2
    centered.paste(resized, (paste_x, paste_y))

    # Scale pixel values from the 0-255 range to the 0-1 range the model
    # was trained on.
    pixels = np.array(centered, dtype=np.float64) / 255.0
    return pixels.reshape(1, -1)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)
    if not data or "image" not in data:
        return jsonify({"error": "Missing image data"}), 400

    image = decode_canvas_image(data["image"])
    features = preprocess_image(image)

    if features.max() == 0:
        return jsonify({"error": "Empty drawing"}), 400

    prediction = int(model.predict(features)[0])
    return jsonify({"digit": prediction})


if __name__ == "__main__":
    app.run(debug=True)
