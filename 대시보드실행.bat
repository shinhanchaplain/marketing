@echo off
setlocal
cd /d "%~dp0"
python start.py
if %ERRORLEVEL% NEQ 0 (
    pause
)
