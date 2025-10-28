<#
.SYNOPSIS
  Post-build script to run on Windows to create a single EXE, embed icon and version info, and optionally sign.

USAGE
  Run this from the repository root on Windows PowerShell (run as Administrator for signing):

    .\tools\build_windows_post.ps1 -Version 1.0 -IconPath .\offline_ui\public\cridergpt.ico -CertPath C:\path\to\cert.pfx -CertPassword 'password'

DESCRIPTION
  This script assumes you have already prepared the build payload with:
    python tools\build_windows.py --prepare --version 1.0 --icon offline_ui\public\cridergpt.ico

  It then runs PyInstaller (requires pyinstaller on PATH), uses rcedit.exe (if present)
  to set version metadata and icon, and optionally signs the binary with signtool.

  See tools\BUILD_POSTREADME.md for prerequisites and notes.
#>

param(
    [string]$Version = "1.0",
    [string]$IconPath = "offline_ui\public\cridergpt.ico",
    [string]$CertPath = "",
    [string]$CertPassword = "",
    [switch]$VerboseMode
)

Set-StrictMode -Version Latest

$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
Push-Location $RepoRoot

if (-not (Test-Path $IconPath)) {
    Write-Host "Icon not found at $IconPath. Please provide a valid .ico file." -ForegroundColor Yellow
}

$buildDir = Join-Path $RepoRoot 'build\cridergpt_app'
if (-not (Test-Path $buildDir)) {
    Write-Error "Build folder $buildDir not found. Run python tools\build_windows.py --prepare first."; exit 1
}

$exeName = "CriderGPT_Offline_v$Version.exe"

Write-Host "Running PyInstaller to build $exeName..."

# Build command
$pyinstallerArgs = @(
    '--onefile',
    '--noconsole',
    "--name=$exeName",
    "--add-data=$($buildDir)\www;www",
    "--add-data=$($buildDir)\agent;agent",
    "--add-data=$($buildDir)\offline_logs;offline_logs",
    "--add-data=$($buildDir)\shadow;shadow",
)
if (Test-Path $IconPath) { $pyinstallerArgs += "--icon=$IconPath" }

& pyinstaller @pyinstallerArgs main.py
if ($LASTEXITCODE -ne 0) { Write-Error "PyInstaller failed with exit code $LASTEXITCODE"; exit $LASTEXITCODE }

$distExe = Join-Path $RepoRoot "dist\$exeName"
if (-not (Test-Path $distExe)) { Write-Error "Expected exe not found at $distExe"; exit 1 }

# Move exe to build folder
Copy-Item $distExe -Destination (Join-Path $buildDir $exeName) -Force

# Apply version info and icon using rcedit if available
$rcedit = Join-Path $RepoRoot 'tools\rcedit.exe'
if (Test-Path $rcedit) {
    Write-Host "Applying version info and icon via rcedit..."
    $meta = Get-Content -Raw -Path (Join-Path $RepoRoot 'tools\version_metadata.json') | ConvertFrom-Json
    $target = Join-Path $buildDir $exeName
    # Set file version and product version
    & $rcedit $target --set-version-string "CompanyName" $meta.CompanyName
    & $rcedit $target --set-version-string "FileDescription" $meta.FileDescription
    & $rcedit $target --set-version-string "ProductName" $meta.ProductName
    & $rcedit $target --set-version-string "OriginalFilename" $meta.OriginalFilename
    & $rcedit $target --set-version-string "LegalCopyright" $meta.LegalCopyright
    if (Test-Path $IconPath) {
        & $rcedit $target --set-icon $IconPath
    }
} else {
    Write-Host "rcedit.exe not found in tools/. Skipping version embedding step. You can download rcedit from https://github.com/electron/rcedit" -ForegroundColor Yellow
}

# Optionally sign the binary
if ($CertPath -and (Test-Path $CertPath)) {
    $signtool = "signtool"
    Write-Host "Signing binary with cert $CertPath"
    & $signtool sign /f $CertPath /p $CertPassword /tr http://timestamp.digicert.com /td SHA256 /fd SHA256 (Join-Path $buildDir $exeName)
    if ($LASTEXITCODE -ne 0) { Write-Error "signtool failed with exit code $LASTEXITCODE" }
}

# Generate SHA256 checksum
$outExe = Join-Path $buildDir $exeName
$hashOut = Join-Path $RepoRoot 'build\verify.log'
Write-Host "Generating SHA256 hash to $hashOut"
certutil -hashfile $outExe SHA256 | Out-File -FilePath $hashOut -Encoding ascii

Write-Host "Build complete. EXE located at: $outExe"

# Create desktop shortcut (for current user)
$desktop = [Environment]::GetFolderPath('Desktop')
$lnk = Join-Path $desktop 'CriderGPT Offline.lnk'
if (-not (Test-Path $lnk)) {
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut($lnk)
    $shortcut.TargetPath = $outExe
    $shortcut.IconLocation = $outExe
    $shortcut.Save()
    Write-Host "Desktop shortcut created: $lnk"
} else { Write-Host "Desktop shortcut already exists: $lnk" }

Pop-Location
