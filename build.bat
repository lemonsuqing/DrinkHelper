@echo off
echo ========= Build DrinkHelper =========

:: 切换到脚本所在目录
cd /d %~dp0

where pyinstaller >nul 2>nul
if errorlevel 1 (
   echo [ERROR] there is not 'pyinstaller'，pless run 'pip install pyinstaller' in your shell
    pause
    exit /b
)

pyinstaller main.py --noconsole --onefile --add-data "assets\icon.ico;assets" --icon=assets\icon.ico --name=WaterReminder

echo [OK] Build success, the file in 'dist\WaterReminder.exe'
pause
