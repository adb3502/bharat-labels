@echo off
title BHARAT Labels Server (Local Network)

echo ========================================
echo   BHARAT Study Label Generator
echo   Local Network Access
echo ========================================
echo.

cd /d "%~dp0"

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Get local IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    for /f "tokens=1" %%b in ("%%a") do set LOCAL_IP=%%b
)

echo Your local IP: %LOCAL_IP%
echo.
echo ========================================
echo   Access the app at:
echo   http://%LOCAL_IP%:8501
echo ========================================
echo.
echo Share this URL with others on the lab network.
echo.
echo Press Ctrl+C to stop the server.
echo.

:: Start Streamlit accessible on local network
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
