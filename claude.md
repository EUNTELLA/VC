# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository overview

This is a coursework repository ("VC") organized by week. Each `weekNN/`
folder holds that week's exercises. A week's exercises may be split into
independent sub-projects (e.g. a desktop version and a web version of the
same program), each in its own subfolder with its own `claude.md`,
`requirements.txt`, and dependencies. Always check for a `claude.md`
inside the specific subfolder you're working in — it documents that
sub-project's purpose, stack, and run commands more specifically than
this top-level file.

Current contents:
- `week03/desktop_version/` — Tkinter GUI where the user draws a digit
  and a trained scikit-learn model predicts it. Fully implemented.
- `week03/web_version/` — Flask + HTML5 canvas equivalent of the desktop
  version (same model, browser-based drawing UI). Fully implemented.
- `week04/` — Personal to-do list app (plain HTML/CSS/JS, no server,
  `localStorage` persistence). See `week04/PRD.md` and
  `week04/claude.md`. Fully implemented.

## Commands

Python is not on PATH by default in a fresh shell in this environment.
If `python` is not found, refresh PATH in the current PowerShell session
before running any command below:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable('Path','Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path','User')
```

Each sub-project is self-contained. From inside a sub-project folder:
```
pip install -r requirements.txt
python train_model.py              # trains the model, saves to model/digit_model.joblib
python digit_recognizer_gui.py     # desktop_version: launches the Tkinter drawing GUI
python app.py                      # web_version: starts the Flask server (http://127.0.0.1:5000)
```
Each sub-project also has a `Run_*.bat` file (e.g.
`desktop_version/Run_Digit_Recognizer.bat`,
`web_version/Run_Web_App.bat`) that can be double-clicked from Windows
Explorer instead: it trains the model on first run if missing, then
launches the app. These scripts call `python.exe` by absolute path
rather than relying on PATH, since Explorer may not see a PATH update
from a Python install done earlier in the same login session.

There is no repo-wide build, lint, or test command — each sub-project
manages its own dependencies and is run directly with `python`.

`train_model.py` scripts that use `fetch_openml` need internet access
and `pandas` (required by `fetch_openml` itself). If it fails with
`CERTIFICATE_VERIFY_FAILED`, the `pip-system-certs` package (in each
sub-project's `requirements.txt`) fixes it by making Python use the OS
certificate store — this is commonly needed on a fresh python.org
install on Windows.

## Coding rules

- All code and comments in this repository are written in English, even
  when instructions/discussion happen in another language. User-facing
  UI text (button labels, category names, etc.) may be Korean when the
  app targets a Korean-speaking user — see `week04/app.js`
  (`CATEGORY_LABELS`) for the pattern: English identifiers internally,
  Korean strings only at the point they're shown to the user.
- Every new file must start with a comment stating its creation date and
  time (local time, `YYYY-MM-DD HH:MM:SS` format), e.g.:
  ```python
  # Created: 2026-09-17 10:31:27
  ```
  Use the appropriate comment syntax for the file type (`#` for Python,
  `//` for JS, `<!-- -->` for HTML/Markdown, etc.). Get the real current
  date/time rather than guessing it.
- Keep comments minimal: only explain non-obvious *why*, not *what* —
  existing scripts (`train_model.py`, `digit_recognizer_gui.py`) are the
  style reference (short module docstring at the top, constants in
  `UPPER_SNAKE_CASE`, no inline comments unless a step is genuinely
  surprising).

## ML/data conventions

- ML sub-projects in this repo train on the MNIST dataset (28x28
  grayscale digit images, ~70,000 samples) via `sklearn.datasets.
  fetch_openml`. An 8x8 `sklearn.datasets.load_digits` model was tried
  first for full offline use, but was dropped: it comes from a
  different low-resolution optical-scanner pipeline and generalizes
  poorly to real freehand mouse-drawn digits.
- Any prediction pipeline (e.g. a drawn image) must reproduce MNIST's
  own framing convention to get good accuracy: crop to the bounding box
  of the drawn strokes, scale the longest side to fit a 20x20 box
  (preserving aspect ratio), paste it centered onto a blank 28x28
  canvas, then scale pixel values from 0-255 to 0-1. A naive full-canvas
  resize to 28x28 performs noticeably worse.
- Trained models are saved with `joblib` to a `model/` folder local to
  each sub-project (not shared/committed across sub-projects).
