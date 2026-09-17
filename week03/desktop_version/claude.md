# Desktop Version — Handwritten Digit Recognizer

## Purpose
A native desktop application (Tkinter GUI) where the user draws a digit
with the mouse and a trained machine learning model predicts which digit
(0-9) it is.

## Tech stack
- Python 3.12
- Tkinter (built-in GUI toolkit, canvas for drawing)
- scikit-learn (`MLPClassifier` trained on the MNIST dataset via
  `fetch_openml`)
- Pillow (mirrors canvas strokes into an in-memory image, crops/centers
  it for prediction)
- joblib (saves/loads the trained model)

## Files
- `train_model.py` — downloads MNIST (first run only, needs internet;
  cached by scikit-learn after that), trains an MLP classifier, and
  saves it to `model/digit_model.joblib`.
- `digit_recognizer_gui.py` — launches the drawing GUI, loads the saved
  model, and predicts the digit drawn by the user.
- `requirements.txt` — Python dependencies for this version.
- `Run_Digit_Recognizer.bat` — double-clickable launcher (Windows
  Explorer): trains the model on first run if missing, then opens the
  GUI. Uses an absolute path to `python.exe` so it works even if
  Explorer's PATH hasn't picked up a newly installed Python yet.

## How to run
```
pip install -r requirements.txt
python train_model.py
python digit_recognizer_gui.py
```
Or just double-click `Run_Digit_Recognizer.bat`.

## Notes
- All code and comments are written in English.
- The model is trained on 28x28 MNIST images. The canvas drawing is
  cropped to its bounding box, scaled to fit a 20x20 box, and centered
  on a 28x28 canvas before prediction — this mirrors MNIST's own
  preprocessing convention and matters a lot for accuracy on freehand
  mouse drawings (a naive full-canvas resize performed noticeably
  worse). `load_digits` (8x8) was tried first but dropped: it comes
  from a different low-resolution optical-scanner pipeline and
  generalizes poorly to mouse-drawn digits.
- SSL certificate verification for `fetch_openml` on a fresh
  python.org install on Windows may fail
  (`CERTIFICATE_VERIFY_FAILED`) until the `pip-system-certs` package is
  installed, which makes Python use the OS certificate store.
