# Created: 2026-09-17 10:32:30
"""Train a handwritten digit classifier and save it to disk.

Uses the MNIST dataset (28x28 grayscale images of digits 0-9, ~70,000
samples) via scikit-learn's `fetch_openml`, since it is much more
representative of real freehand mouse-drawn digits than the small 8x8
`load_digits` dataset (which comes from a different, low-resolution
optical scanner pipeline and generalizes poorly to canvas drawings).
Requires internet access the first time it is run (the dataset is then
cached locally by scikit-learn). Mirrors desktop_version/train_model.py
so both versions use the same model format.
"""

import os

import joblib
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score

MODEL_DIR = os.path.join(os.path.dirname(__file__), "model")
MODEL_PATH = os.path.join(MODEL_DIR, "digit_model.joblib")


def train_and_save_model():
    # Load the 28x28 MNIST handwritten digit images and their labels.
    mnist = fetch_openml("mnist_784", version=1, as_frame=False)
    X = mnist.data.astype("float64") / 255.0  # scale pixels to 0-1
    y = mnist.target.astype("int64")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # A small MLP gives strong accuracy on MNIST while keeping the saved
    # model file small and prediction fast (unlike e.g. a kernel SVM or
    # k-NN, which would need to keep the whole training set around).
    model = MLPClassifier(
        hidden_layer_sizes=(128, 64),
        max_iter=30,
        early_stopping=True,
        random_state=42,
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Test accuracy: {accuracy:.4f}")

    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    train_and_save_model()
