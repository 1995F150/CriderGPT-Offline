<#
PowerShell helper to build a single-file EXE with PyInstaller and compile an Inno Setup installer.

Run on Windows (Administrator recommended):
  Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
  .\tools\build_installer.ps1 -IconPath ".\ui\assets\cridergpt.ico"

This script will:
- Run PyInstaller to produce dist\CriderGPT_Offline.exe
- Create the Inno Setup script (build_installer.iss is expected at repo root)
- Run ISCC.exe to build the installer if Inno Setup is installed

Note: This script assumes Python, PyInstaller, and Inno Setup are installed on the Windows build machine.
#>

param(
    [string]$IconPath = ".\ui\assets\cridergpt.ico",
    [string]$PyInstallerExe = "pyinstaller",
    [string]$ISCCPath = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
)

function Write-Log { param($m); Write-Host "[build] $m" }

Write-Log "Starting PyInstaller build (onefile, windowed)"

$pyCmd = "{0} --onefile --windowed main.py --icon=`"{1}`" --name=`"CriderGPT_Offline`"" -f $PyInstallerExe $IconPath

# Execute PyInstaller
Write-Log "Running: pyinstaller --onefile --windowed main.py --icon=\"$IconPath\" --name=CriderGPT_Offline"
& pyinstaller --onefile --windowed main.py --icon="$IconPath" --name="CriderGPT_Offline"

if (-not (Test-Path .\dist\CriderGPT_Offline.exe)) {
    Write-Log "ERROR: dist\CriderGPT_Offline.exe not found. PyInstaller failed."
    exit 1
}

Write-Log "PyInstaller succeeded. Checking for build_installer.iss"
if (-not (Test-Path ..\build_installer.iss -PathType Leaf)) {
    Write-Log "build_installer.iss not found at repo root. Ensure it's present and re-run."
} else {
    if (Test-Path $ISCCPath) {
        Write-Log "Running Inno Setup Compiler: $ISCCPath build_installer.iss"
        & "$ISCCPath" ..\build_installer.iss
        if ($LASTEXITCODE -eq 0) {
            Write-Log "Installer created in dist\CriderGPT_Offline_Setup.exe"
        } else {
            Write-Log "ISCC failed with exit code $LASTEXITCODE"
        }
    } else {
        Write-Log "ISCC.exe not found at $ISCCPath. Please install Inno Setup or update the path."
    }
}

Write-Log "All done. Verify dist folder for outputs."
