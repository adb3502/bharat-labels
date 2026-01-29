@echo off
echo Removing PDF worker service...
taskkill /f /im pythonw.exe 2>nul
schtasks /delete /tn "BHARAT_Worker" /f 2>nul
del "%~dp0worker_hidden.vbs" 2>nul
echo Done.
pause
