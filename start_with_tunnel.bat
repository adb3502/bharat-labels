@echo off
title BHARAT Labels Server (Public)

echo ========================================
echo   BHARAT Study Label Generator
echo   Public Access via Cloudflare Tunnel
echo ========================================
echo.

cd /d "%~dp0"

:: Check cloudflared
where cloudflared >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] cloudflared not installed!
    echo Run: winget install Cloudflare.cloudflared
    pause
    exit /b 1
)

:: Kill existing Streamlit if running
taskkill /f /im streamlit.exe >nul 2>&1
timeout /t 2 /nobreak >nul

:: Activate venv
call venv\Scripts\activate.bat

echo Starting Streamlit...
start /b streamlit run app.py --server.address 0.0.0.0 --server.port 8501 --server.headless true

:: Wait for Streamlit
timeout /t 5 /nobreak >nul

echo Starting Cloudflare Tunnel...
echo.
echo ========================================
echo   Your public URL will appear below:
echo ========================================
echo.

cloudflared tunnel --url http://localhost:8501
