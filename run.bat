@echo off
title DocAgent AI - Policy & Handbook Assistant
echo ==========================================================
echo           DocAgent AI Launcher & Setup
echo ==========================================================
echo.

:: 1. Check Python Installation
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python 3.9 or higher and try again.
    echo.
    pause
    exit /b 1
)

:: 2. Setup Virtual Environment
if not exist ".venv" (
    echo [INFO] Creating Python virtual environment in .venv...
    python -m venv .venv
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
    echo [INFO] Virtual environment created successfully.
)

:: 3. Activate Virtual Environment
echo [INFO] Activating virtual environment...
call .venv\Scripts\activate

:: 4. Install Dependencies
echo [INFO] Upgrading pip...
.\.venv\Scripts\python.exe -m pip install --upgrade pip >nul 2>nul

echo [INFO] Installing required packages...
.\.venv\Scripts\pip.exe install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Package installation failed. Please check your internet connection.
    pause
    exit /b 1
)

:: 5. Setup & Build Frontend (Vue 3 + Vite)
if exist "frontend\package.json" (
    where npm >nul 2>nul
    if %errorlevel% equ 0 (
        if not exist "frontend\node_modules" (
            echo [INFO] Installing frontend dependencies...
            pushd frontend
            call npm install
            popd
        )
        echo [INFO] Building latest Vue frontend...
        pushd frontend
        call npm run build
        popd
    ) else (
        if not exist "frontend\dist" (
            echo [WARN] npm is not found in PATH. Make sure Node.js is installed to build frontend.
        )
    )
)

:: 6. Initialize directories & start server
echo [INFO] Starting application server...
echo.
echo ==========================================================
echo   DocAgent AI is running at: http://localhost:8000
echo   Frontend (Vue 3):          http://localhost:8000/
echo   API documentation:         http://localhost:8000/docs
echo ==========================================================
echo.
.\.venv\Scripts\uvicorn.exe main:app --host 127.0.0.1 --port 8000 --reload

pause
