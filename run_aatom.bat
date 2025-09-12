@echo off
cd /d "%~dp0"
setlocal

set "VENV_DIR=.venv"

if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
    call "%VENV_DIR%\Scripts\activate.bat"
    if exist requirements.txt (
        echo Installing dependencies...
        python -m pip install --upgrade pip
        python -m pip install -r requirements.txt
    )
) else (
    call "%VENV_DIR%\Scripts\activate.bat"
)

python -m aatom_desktop
