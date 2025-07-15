@echo off
cd /d %~dp0

REM ================================================
REM WaterReminder Build Script
REM Copyright (c) 2025 Lemonsuqing. All rights reserved.
REM
REM This build script is part of the WaterReminder project.
REM Unauthorized copying or distribution is prohibited.
REM ================================================

REM Check and install pyinstaller
pip show pyinstaller >nul 2>nul
if errorlevel 1 (
    echo [INFO] pyinstaller not found, installing from PyPI...
    pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install pyinstaller!
        pause
        exit /b
    )
) else (
    echo [INFO] pyinstaller already installed.
)

REM Check and install PyQt6
pip show PyQt6 >nul 2>nul
if errorlevel 1 (
    echo [INFO] PyQt6 not found, installing from PyPI...
    pip install PyQt6
    if errorlevel 1 (
        echo [ERROR] Failed to install PyQt6!
        pause
        exit /b
    )
) else (
    echo [INFO] PyQt6 already installed.
)

REM Start building
echo [INFO] Building WaterReminder...
pyinstaller source\main.py --noconsole --onefile --add-data "assets\icon.ico;assets" --icon=assets\icon.ico --name=WaterReminder --distpath .

if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b
) else (
    echo [OK] Build success, the file is in 'WaterReminder.exe'
    pause
)
