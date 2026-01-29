@echo off
title BHARAT Labels - PDF Worker
cd /d "%~dp0"
call venv\Scripts\activate.bat
python convert_worker.py
pause
