@echo off
REM Define the URL for the Python installer
SET PYTHON_URL=https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe
SET PYTHON_INSTALLER=python-installer.exe
cd /d %~dp0

REM Check if Python is already installed
where python >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    echo Python is already installed.
    GOTO APP
)

REM Print the current download directory
echo Downloading Python to: %CD%
echo .

REM Download Python installer using curl or PowerShell
curl -o %PYTHON_INSTALLER% %PYTHON_URL% || powershell -Command "Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'"

REM Check if the installer was downloaded
IF NOT EXIST %PYTHON_INSTALLER% (
    echo Failed to download Python installer.
    exit /B
)
echo Installing Python, please wait
echo.
REM Install Python silently and add to PATH
START /WAIT %PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

timeout /t 5 /nobreak >nul

REM Optionally install pip
py -m ensurepip

REM Clean up installer
DEL %PYTHON_INSTALLER%

echo Python installation with PIP and Path is complete!

timeout /t 5 /nobreak >nul
echo Starting App
timeout /t 5 /nobreak >nul
echo Press Ctrl + C to stop this app, or just close it.
echo.

:APP
cd /d "%~dp0"
py app.py
