@echo off
cd /d "%~dp0"

if exist "venv\Scripts\activate.bat" call venv\Scripts\activate.bat

python -c "from run_config import launch_gui; launch_gui(1)"
pause
