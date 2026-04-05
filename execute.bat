@echo off 

cd /d "%~dp0"

python --version >nul 2>&1

IF ERRORLEVEL 1 (
    echo [ERROR] Python is not installed 
    exit /b 1
)

echo Upgrading PIP
python -m pip install --upgrade pip 

IF EXIST requirements.txt (
    echo installing dependencies
    python -m pip install -r requirements.txt 
)

echo Running Python Script
python main.py 

echo . 
echo Finished Script 
pause 