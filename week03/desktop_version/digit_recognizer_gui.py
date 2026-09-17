"""Desktop GUI for handwritten digit recognition.

The user draws a digit with the mouse on a canvas. The drawing is mirrored
onto an in-memory image, cropped to the drawn strokes and centered onto a
28x28 canvas (matching the MNIST convention the model was trained on),
and classified when the "Predict" button is pressed.
"""

import os
import tkinter as tk
from tkinter import messagebox

import joblib
import numpy as np
from PIL import Image, ImageDraw

MODEL_PATH = os.path.join(os.path.dirname(__file__), "model", "digit_model.joblib")

# The drawing canvas is scaled up for easier drawing; the trained model
# expects 28x28 images, matching the MNIST dataset.
CANVAS_SIZE = 280
MODEL_IMAGE_SIZE = 28
DIGIT_BOX_SIZE = 20  # the drawn digit is scaled to fit within this box,
                     # leaving a border, matching classic MNIST preprocessing
BRUSH_RADIUS = 10


class DigitRecognizerApp:
    def __init__(self, root, model):
        self.root = root
        self.model = model
        self.root.title("Handwritten Digit Recognizer")

        self.last_x = None
        self.last_y = None

        # Visible drawing canvas (black background, white strokes).
        self.canvas = tk.Canvas(
            root, width=CANVAS_SIZE, height=CANVAS_SIZE, bg="black", cursor="cross"
        )
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Off-screen image that mirrors the canvas strokes, used for prediction.
        self.image = Image.new("L", (CANVAS_SIZE, CANVAS_SIZE), color=0)
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.bind("<Button-1>", self.on_start)
        self.canvas.bind("<B1-Motion>", self.on_draw)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.result_label = tk.Label(root, text="Draw a digit (0-9)", font=("Arial", 20))
        self.result_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        predict_button = tk.Button(root, text="Predict", command=self.predict_digit)
        predict_button.grid(row=2, column=0, padx=10, pady=10)

        clear_button = tk.Button(root, text="Clear", command=self.clear_canvas)
        clear_button.grid(row=2, column=1, padx=10, pady=10)

        quit_button = tk.Button(root, text="Quit", command=root.destroy)
        quit_button.grid(row=2, column=2, padx=10, pady=10)

    def on_start(self, event):
        self.last_x, self.last_y = event.x, event.y

    def on_draw(self, event):
        x, y = event.x, event.y
        if self.last_x is not None:
            # Draw on the visible canvas.
            self.canvas.create_line(
                self.last_x, self.last_y, x, y,
                width=BRUSH_RADIUS * 2, fill="white",
                capstyle=tk.ROUND, smooth=True,
            )
            # Mirror the same stroke on the off-screen image used for prediction.
            self.draw.line(
                [self.last_x, self.last_y, x, y],
                fill=255, width=BRUSH_RADIUS * 2,
            )
        self.last_x, self.last_y = x, y

    def on_release(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, CANVAS_SIZE, CANVAS_SIZE], fill=0)
        self.result_label.config(text="Draw a digit (0-9)")

    def preprocess_image(self):
        # Crop to the bounding box of the drawn strokes (ignore empty margins).
        bbox = self.image.getbbox()
        if bbox is None:
            return np.zeros((1, MODEL_IMAGE_SIZE * MODEL_IMAGE_SIZE))
        cropped = self.image.crop(bbox)

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

        # Scale pixel values from the 0-255 range to the 0-1 range the
        # model was trained on.
        pixels = np.array(centered, dtype=np.float64) / 255.0
        return pixels.reshape(1, -1)

    def predict_digit(self):
        features = self.preprocess_image()
        if features.max() == 0:
            messagebox.showinfo("No drawing", "Please draw a digit first.")
            return

        prediction = self.model.predict(features)[0]
        self.result_label.config(text=f"Predicted digit: {prediction}")


def main():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model not found at {MODEL_PATH}. Run train_model.py first."
        )

    model = joblib.load(MODEL_PATH)

    root = tk.Tk()
    DigitRecognizerApp(root, model)
    root.mainloop()


if __name__ == "__main__":
    main()
