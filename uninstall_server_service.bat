@echo off
echo Removing server service...
taskkill /f /im streamlit.exe >nul 2>&1
taskkill /f /im cloudflared.exe >nul 2>&1
schtasks /delete /tn "BHARAT_Server" /f >nul 2>&1
del "%~dp0server_hidden.vbs" 2>nul
del "%~dp0server_runner.py" 2>nul
echo Done.
pause
