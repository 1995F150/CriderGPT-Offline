<#
Full Windows build automation for CriderGPT Offline.

Usage (run as Administrator on Windows build machine):
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
    .\tools\build_windows_full.ps1 -Version "1.0.0" -IconPath ".\offline_ui\public\cridergpt.ico" -SignCertPath "C:\keys\codesign.pfx" -SignCertPassword "PFXPASS" -MakeInstaller

This script will:
- install Python deps (if requested),
- run PyInstaller using the provided spec or a generated command,
- run the post-processing to apply version metadata and icon (rcedit),
- optionally sign the executable (signtool),
- optionally create an Inno Setup installer if ISCC.exe is available.

Notes:
- Ensure rcedit.exe is in PATH or in the same directory as this script.
- Ensure PyInstaller is installed in the active Python environment.
- Running this requires a Windows environment; this script will not run in Linux.
#>

param(
    [string]$Version = "1.0.0",
    [string]$IconPath = ".\offline_ui\public\cridergpt.ico",
    [string]$VersionFile = ".\tools\version_metadata.json",
    [string]$SpecFile = ".\tools\cridergpt.spec",
    [string]$ExeName = "CriderGPT-Offline.exe",
    [string]$SignCertPath = "",
    [string]$SignCertPassword = "",
    [switch]$MakeInstaller
)

function Write-Log {
    param($msg)
    Write-Host "[build] $msg"
}

Write-Log "Starting full Windows build. Version=$Version"

if (-not (Test-Path $IconPath)) {
    Write-Log "Warning: Icon not found at $IconPath. Continue? (y/n)"
    $c = Read-Host
    if ($c -ne 'y') { throw "Icon missing" }
}

Write-Log "Ensure Python venv and PyInstaller are installed (you can skip if satisfied)."
Write-Log "Activate your build environment now (or press Enter to continue)."
Read-Host -Prompt "Press Enter to continue when ready"

# Run PyInstaller
if (Test-Path $SpecFile) {
    Write-Log "Running PyInstaller with spec: $SpecFile"
    pyinstaller --clean --noconfirm $SpecFile
} else {
    $pyCmd = "pyinstaller --clean --noconfirm --onefile --windowed --name \"CriderGPT-Offline\" --icon \"$IconPath\" --add-data \"build\\cridergpt_app\\www;www\" main.py"
    Write-Log "Spec file not found; using generated command: $pyCmd"
    Invoke-Expression $pyCmd
}

$distExe = Join-Path -Path (Get-Location) -ChildPath "dist\CriderGPT-Offline.exe"
if (-not (Test-Path $distExe)) {
    Write-Log "ERROR: Expected EXE not found at $distExe"
    exit 1
}

Write-Log "Applying version metadata and icon via build_windows_post.ps1"
.\tools\build_windows_post.ps1 -ExePath $distExe -VersionFile $VersionFile -IconPath $IconPath

if ($SignCertPath -and (Test-Path $SignCertPath)) {
    Write-Log "Signing EXE with certificate $SignCertPath"
    .\tools\build_windows_post.ps1 -ExePath $distExe -VersionFile $VersionFile -IconPath $IconPath -SignCertPath $SignCertPath -SignCertPassword $SignCertPassword
}

if ($MakeInstaller) {
    $iss = Join-Path -Path (Get-Location) -ChildPath "tools\installer\cridergpt_installer.iss"
    if (-not (Test-Path $iss)) { Write-Log "Installer script not found: $iss"; exit 1 }
    if (Get-Command ISCC.exe -ErrorAction SilentlyContinue) {
        Write-Log "Building Inno Setup installer"
        & ISCC.exe $iss
        Write-Log "Installer created"
    } else {
        Write-Log "ISCC.exe (Inno Setup Compiler) not found in PATH. Skipping installer creation."
    }
}

Write-Log "Build finished. Dist folder contains the produced EXE."
