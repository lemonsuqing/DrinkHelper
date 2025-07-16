@echo off
cd /d %~dp0

REM ================================================
REM WaterReminder Uninstall Script
REM Copyright (c) 2025 Lemonsuqing. All rights reserved.
REM ================================================

echo ===============================
echo Cleaning up WaterReminder project build files...
echo ===============================

REM Delete build folder
if exist build (
    rmdir /s /q build
    echo Deleted build folder
) else (
    echo build folder does not exist
)

REM Delete dist folder
if exist dist (
    rmdir /s /q dist
    echo Deleted dist folder
) else (
    echo dist folder does not exist
)

REM Delete WaterReminder.spec file
if exist WaterReminder.spec (
    del /f WaterReminder.spec
    echo Deleted WaterReminder.spec file
) else (
    echo WaterReminder.spec file does not exist
)

REM Delete WaterReminder.exe file
if exist WaterReminder.exe (
    del /f WaterReminder.exe
    echo Deleted WaterReminder.exe file
) else (
    echo WaterReminder.exe file does not exist
)

REM Delete water_reminder_config.json file
if exist water_reminder_config.json (
    del /f water_reminder_config.json
    echo Deleted water_reminder_config.json
) else (
    echo water_reminder_config.json does not exist
)

echo ===============================
echo Cleanup completed!
echo ===============================
pause
