@echo off
title Install BHARAT Server Service

echo ========================================
echo   Install Web Server + Tunnel Service
echo ========================================
echo.
echo This will run Streamlit and Cloudflare Tunnel
echo in the background, starting at logon.
echo.
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

:: Make sure output folder exists
if not exist "%SCRIPT_DIR%\output" mkdir "%SCRIPT_DIR%\output"

:: Create batch file that runs both (simpler approach)
(
echo @echo off
echo cd /d "%SCRIPT_DIR%"
echo call venv\Scripts\activate.bat
echo start /b streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true
echo timeout /t 5 /nobreak ^>nul
echo cloudflared tunnel --url http://localhost:8501 ^> "%SCRIPT_DIR%\output\server.log" 2^>^&1
) > "%SCRIPT_DIR%\run_server.bat"

:: Create VBS to run hidden
(
echo Set WshShell = CreateObject^("WScript.Shell"^)
echo WshShell.Run """%SCRIPT_DIR%\run_server.bat""", 0, False
) > "%SCRIPT_DIR%\server_hidden.vbs"

:: Delete old task and processes
schtasks /delete /tn "BHARAT_Server" /f >nul 2>&1
taskkill /f /im streamlit.exe >nul 2>&1
taskkill /f /im cloudflared.exe >nul 2>&1

:: Create task
schtasks /create /tn "BHARAT_Server" /tr "wscript.exe \"%SCRIPT_DIR%\server_hidden.vbs\"" /sc onlogon /rl highest /f

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Server service installed!
    echo.
    echo Starting server now...

    timeout /t 2 /nobreak >nul
    schtasks /run /tn "BHARAT_Server"

    echo.
    echo Waiting for tunnel URL...
    timeout /t 20 /nobreak

    echo.
    echo Your tunnel URL:
    type "%SCRIPT_DIR%\output\server.log" 2>nul | findstr /i "trycloudflare.com"

    echo.
    echo The server will now:
    echo   - Start automatically when you log in
    echo   - Run silently in the background
    echo.
    echo To get URL: get_url.bat
    echo To stop: stop_server.bat
) else (
    echo [ERROR] Failed to create task
)

pause
