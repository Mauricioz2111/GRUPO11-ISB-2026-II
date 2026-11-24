$ErrorActionPreference = "Stop"

$Carpeta = Split-Path -Parent $MyInvocation.MyCommand.Path
$Python = Join-Path $Carpeta ".venv\Scripts\python.exe"
$Pythonw = Join-Path $Carpeta ".venv\Scripts\pythonw.exe"
$Launcher = Join-Path $Carpeta "launcher.py"
$Requirements = Join-Path $Carpeta "requirements.txt"

if (-not (Test-Path $Python)) {
    Write-Host "No se encontró el entorno virtual .venv." -ForegroundColor Yellow
    Write-Host "Créalo primero con: python -m venv .venv"
    exit 1
}

Write-Host "Instalando dependencias de EOG-Adapta..." -ForegroundColor Cyan
& $Python -m pip install -r $Requirements

if ($LASTEXITCODE -ne 0) {
    Write-Host "No se pudieron instalar las dependencias." -ForegroundColor Red
    exit $LASTEXITCODE
}

$Escritorio = [Environment]::GetFolderPath("Desktop")
$Acceso = Join-Path $Escritorio "EOG-Adapta.lnk"
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($Acceso)
$Shortcut.TargetPath = $Pythonw
$Shortcut.Arguments = '"' + $Launcher + '"'
$Shortcut.WorkingDirectory = $Carpeta
$Shortcut.Description = "Interfaz de comunicación controlada mediante señales EOG"
$Shortcut.IconLocation = "$Pythonw,0"
$Shortcut.Save()

Write-Host "" 
Write-Host "Instalación completada." -ForegroundColor Green
Write-Host "Se creó el acceso directo EOG-Adapta en el escritorio."
Write-Host "Ya puede cerrar esta ventana y abrir la aplicación con doble clic."
