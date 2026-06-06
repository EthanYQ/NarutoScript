@echo off
cd /d "%~dp0"

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [NarutoScript] venv activated
)

python run_config.py 1
pause
