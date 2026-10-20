@echo off
setlocal
cd /d "%~dp0"

echo Starting AI Marketing Studio...
python -m streamlit run app.py

if %ERRORLEVEL% NEQ 0 (
    pause
)
