# PowerShell helper to mark knowledge.json as read-only and restrict write access
$path = Join-Path -Path $PSScriptRoot -ChildPath "..\knowledge\knowledge.json"
if (-Not (Test-Path $path)) { Write-Host "knowledge.json not found at $path"; exit 1 }

# Remove inheritance and grant only read access to Administrators
icacls $path /inheritance:r
icacls $path /grant:r "Administrators:(R)"
icacls $path /deny "Users:(W)"
Write-Host "Applied Windows ACLs to restrict write access to Administrators for: $path"
