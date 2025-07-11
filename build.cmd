@echo off
cd /d %~dp0

REM ================================================
REM WaterReminder Build Script
REM Copyright (c) 2025 Lemonsuqing. All rights reserved.
REM
REM This build script is part of the WaterReminder project.
REM Unauthorized copying or distribution is prohibited.
REM ================================================

REM 检查 Python 环境是否有 pyinstaller
pip show pyinstaller >nul 2>nul
if errorlevel 1 (
    echo [INFO] pyinstaller not found, installing from local wheel...
    pip install tool\pyinstaller-6.14.2-py3-none-win_arm64.whl
    if errorlevel 1 (
        echo [ERROR] Failed to install pyinstaller from local wheel!
        pause
        exit /b
    )
) else (
    echo [INFO] pyinstaller already installed.
)

REM 检查 Python 环境是否有 pyqt6
pip show PyQt6 >nul 2>nul
if errorlevel 1 (
    echo [INFO] PyQt6 not found, installing from local wheel...
    pip install tool\pyqt6-6.9.1-cp39-abi3-win_arm64.whl
    if errorlevel 1 (
        echo [ERROR] Failed to install PyQt6 from local wheel!
        pause
        exit /b
    )
) else (
    echo [INFO] PyQt6 already installed.
)

REM 开始打包
pyinstaller main.py --noconsole --onefile --add-data "assets\icon.ico;assets" --icon=assets\icon.ico --name=WaterReminder --distpath .

if errorlevel 1 (
    echo [ERROR] Build failed!
    pause
    exit /b
) else (
    echo [OK] Build success, the file is in 'dist\WaterReminder.exe'
    pause
)
