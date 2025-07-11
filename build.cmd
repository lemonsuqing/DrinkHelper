@echo off
cd /d %~dp0

REM ================================================
REM WaterReminder Build Script
REM Copyright (c) 2025 Lemonsuqing. All rights reserved.
REM
REM This build script is part of the WaterReminder project.
REM Unauthorized copying or distribution is prohibited.
REM ================================================

where pyinstaller >nul 2>nul
if errorlevel 1 (
   echo [ERROR] there is not 'pyinstaller', pless run 'pip install pyinstaller' in your shell
   pause
   exit /b
)

pyinstaller main.py --noconsole --onefile --add-data "assets\icon.ico;assets" --icon=assets\icon.ico --name=WaterReminder

echo [OK] Build success, the file is in 'dist\WaterReminder.exe'
pause
