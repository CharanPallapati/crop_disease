@echo off
setlocal
cd /d "%~dp0"
echo ==========================================
echo        AgriShield AI - Windows
echo ==========================================
if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)
call "venv\Scripts\activate.bat"
echo Installing/updating dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Dependency installation failed.
    pause
    exit /b 1
)
if not exist ".env" copy /Y ".env.example" ".env" >nul
if not exist "model\disease_model.keras" (
    echo.
    echo WARNING: model\disease_model.keras was not found.
    echo The website will run, but diagnosis will report Model not installed.
)
echo.
echo Starting AgriShield AI...
echo Open http://127.0.0.1:5000/
echo Health check: http://127.0.0.1:5000/api/health
echo Press Ctrl+C to stop.
echo.
python app.py
pause
