# Web Version — Handwritten Digit Recognizer

## Purpose
A browser-based version of the same handwritten digit recognizer: the
user draws a digit on an HTML5 `<canvas>`, the browser sends the drawing
to a small backend, and the predicted digit (0-9) is shown on the page.

## Tech stack
- Python 3.12 + Flask (backend web server and prediction endpoint)
- scikit-learn (`MLPClassifier` trained on the MNIST dataset via
  `fetch_openml`, same as the desktop version)
- HTML5 Canvas + vanilla JavaScript (frontend drawing UI)

## Files
- `train_model.py` — downloads MNIST (first run only, needs internet;
  cached by scikit-learn after that), trains an MLP classifier, and
  saves it to `model/digit_model.joblib` (mirrors the desktop version's
  training script so both versions share the same model format).
- `app.py` — Flask app exposing `/` (drawing page) and `/predict`
  (POST endpoint that receives a base64 canvas PNG, crops/centers it to
  28x28 like MNIST, and returns the predicted digit as JSON:
  `{"digit": <0-9>}` or `{"error": "..."}`).
- `templates/index.html` — the drawing canvas page.
- `static/script.js` — canvas drawing logic + fetch call to `/predict`.
- `requirements.txt` — Python dependencies for this version.
- `Run_Web_App.bat` — double-clickable launcher (Windows Explorer):
  trains the model on first run if missing, starts the Flask server,
  and opens the local URL in the default browser. Uses an absolute path
  to `python.exe` so it works even if Explorer's PATH hasn't picked up a
  newly installed Python yet.

## How to run
```
pip install -r requirements.txt
python train_model.py
python app.py
```
Then open the printed local URL (e.g. http://127.0.0.1:5000) in a
browser. Or just double-click `Run_Web_App.bat`.

## Status
Implemented and verified: server starts, `/predict` correctly classifies
a synthetic drawing sent as a base64 PNG.

## Notes
- All code and comments are written in English.
- Kept independent from `desktop_version/` (own `requirements.txt` and
  training script) so each version can be run and understood on its own.
