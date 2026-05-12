@echo off
echo --- Digital Twin Career Engine Launcher ---
echo.
echo Check: Is Python installed?
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python from python.org
    pause
    exit /b
)

echo 1. Starting Backend Server...
start /b python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000
timeout /t 3 /nobreak > nul

echo 2. Opening Website...
start http://localhost:8000

echo.
echo Running! Keep this window open. 
echo To stop, close this window or press Ctrl+C.
pause
