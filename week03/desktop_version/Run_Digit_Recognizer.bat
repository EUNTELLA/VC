:: Created: 2026-09-17 10:39:42
@echo off
setlocal
set PYTHON_EXE=C:\Users\YUHAN\AppData\Local\Programs\Python\Python312\python.exe
cd /d "%~dp0"

if not exist "model\digit_model.joblib" (
    echo Training the model for the first time - this may take a few minutes...
    "%PYTHON_EXE%" train_model.py
    if errorlevel 1 (
        echo Training failed. See the error above.
        pause
        exit /b 1
    )
)

"%PYTHON_EXE%" digit_recognizer_gui.py
if errorlevel 1 (
    echo The app exited with an error. See above.
    pause
)
