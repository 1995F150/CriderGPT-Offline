<#
Attempts to pin an executable to the Windows taskbar for the current user.
This approach uses the Shell.Application verbs and may not work on all Windows versions
due to security restrictions. Use manually if script fails.

Usage:
  .\tools\pin_taskbar.ps1 -TargetPath 'C:\full\path\to\CriderGPT_Offline_v1.0.exe'
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetPath
)

if (-not (Test-Path $TargetPath)) {
    Write-Error "Target path not found: $TargetPath"; exit 1
}

$shell = New-Object -ComObject Shell.Application
$folder = $shell.Namespace((Split-Path $TargetPath -Parent))
$item = $folder.ParseName((Split-Path $TargetPath -Leaf))

# Find the 'Pin to Taskbar' verb
$verb = $null
foreach ($v in $item.Verbs()) {
    if ($v.Name -match 'Pin to Taskbar|Pin to Tas&kbar') { $verb = $v; break }
}

if ($verb -ne $null) {
    Write-Host "Invoking 'Pin to Taskbar' verb..."
    $verb.DoIt()
    Write-Host "Pinned (or verb invoked)."
} else {
    Write-Warning "Pin verb not available. You may need to pin manually or run as interactive user."
}
