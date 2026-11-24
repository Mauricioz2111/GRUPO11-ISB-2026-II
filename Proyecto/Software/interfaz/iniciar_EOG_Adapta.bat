@echo off
cd /d "%~dp0"

if not exist ".venv\Scripts\pythonw.exe" (
    echo No se encontro el entorno virtual .venv.
    echo Ejecute primero instalar_escritorio.ps1 desde PowerShell.
    pause
    exit /b 1
)

start "" ".venv\Scripts\pythonw.exe" "launcher.py"
exit /b 0
