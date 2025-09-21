@echo off
echo Laptop Testing Program - Launcher
echo ===================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found!
echo.

echo Checking dependencies...
python -c "import PySide6, psutil, cpuinfo, GPUtil; print('All dependencies installed!')" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
)

echo Dependencies OK!
echo.

echo Running module tests...
python test_modules.py
if errorlevel 1 (
    echo ERROR: Module tests failed
    pause
    exit /b 1
)

echo.
echo Starting Laptop Testing Program...
echo.
python script.py

if errorlevel 1 (
    echo.
    echo Application exited with error
    pause
)