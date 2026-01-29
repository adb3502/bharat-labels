@echo off
title Install BHARAT Worker Service

echo ========================================
echo   Install PDF Worker as Scheduled Task
echo ========================================
echo.
echo This will run the PDF worker in the background.
echo Requires Administrator privileges.
echo.
pause

:: Check for admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Run as Administrator!
    pause
    exit /b 1
)

cd /d "%~dp0"
set SCRIPT_DIR=%~dp0
set SCRIPT_DIR=%SCRIPT_DIR:~0,-1%

:: Create VBS to run hidden
echo Set WshShell = CreateObject("WScript.Shell") > "%SCRIPT_DIR%\worker_hidden.vbs"
echo WshShell.Run """%SCRIPT_DIR%\venv\Scripts\pythonw.exe"" ""%SCRIPT_DIR%\convert_worker.py""", 0, False >> "%SCRIPT_DIR%\worker_hidden.vbs"

:: Delete old task
schtasks /delete /tn "BHARAT_Worker" /f >nul 2>&1

:: Create task that runs at logon
schtasks /create /tn "BHARAT_Worker" /tr "wscript.exe \"%SCRIPT_DIR%\worker_hidden.vbs\"" /sc onlogon /rl highest /f

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Worker service installed!
    echo.
    echo Starting worker now...
    schtasks /run /tn "BHARAT_Worker"
    echo.
    echo The worker will now:
    echo   - Start automatically when you log in
    echo   - Run silently in the background
    echo.
    echo To stop: taskkill /f /im pythonw.exe
    echo To uninstall: schtasks /delete /tn "BHARAT_Worker" /f
) else (
    echo [ERROR] Failed to create task
)

pause
