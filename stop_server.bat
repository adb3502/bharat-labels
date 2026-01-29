@echo off
echo Stopping server...
taskkill /f /im streamlit.exe >nul 2>&1
taskkill /f /im cloudflared.exe >nul 2>&1
echo Done.
pause
