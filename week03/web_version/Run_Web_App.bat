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

:: Open the browser a couple seconds after the server starts.
start "" cmd /c "timeout /t 2 >nul && start http://127.0.0.1:5000"

"%PYTHON_EXE%" app.py
if errorlevel 1 (
    echo The server exited with an error. See above.
    pause
)
