@echo off
echo Your public URL:
echo.
type "%~dp0output\server.log" 2>nul | findstr /i "trycloudflare.com"
echo.
pause
