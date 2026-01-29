@echo off
echo Stopping PDF worker...
taskkill /f /im pythonw.exe 2>nul
echo Done.
pause
