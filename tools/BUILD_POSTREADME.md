# Post-build instructions (Windows)

This file explains how `tools/build_windows_post.ps1` works and what you need to provide on Windows to produce a final signed EXE with icon and version metadata.

Prerequisites on Windows build host
- Python 3.10+ and pip
- Node.js and npm (for frontend build)
- PyInstaller (pip install pyinstaller)
- rcedit.exe (optional but recommended) — available from https://github.com/electron/rcedit/releases
- signtool.exe if you want to code-sign (comes with Windows SDK)

Steps
1. Prepare the build payload (from repo root):

```powershell
python tools\build_windows.py --prepare --version 1.0 --icon offline_ui\public\cridergpt.ico
```

2. Run the post-build script which runs PyInstaller and applies metadata:

```powershell
.\tools\build_windows_post.ps1 -Version 1.0 -IconPath .\offline_ui\public\cridergpt.ico
```

3. (Optional) Sign the EXE using a PFX certificate:

```powershell
.\tools\build_windows_post.ps1 -Version 1.0 -IconPath .\offline_ui\public\cridergpt.ico -CertPath C:\path\to\cert.pfx -CertPassword 'yourpass'
```

Notes about the icon
- The repository includes `offline_ui/public/logo.svg` (SVG). Windows executables require an ICO file. Create a `cridergpt.ico` file (multiple sizes inside) and place it in `offline_ui/public/`.
- Tools to create .ico from SVG/PNG: ImageMagick, Inkscape, or online converters. Example using ImageMagick (on Windows with ImageMagick installed):

```powershell
magick convert offline_ui\public\logo.svg -resize 256x256 offline_ui\public\cridergpt.ico
```

Why rcedit
- PyInstaller `--icon` sets the icon, but to add detailed version info or modify existing resource strings after build, `rcedit.exe` is convenient. The post-build script will use `tools/version_metadata.json` if `rcedit.exe` exists in `tools/`.

Verifying icon display
- After creating the EXE, copy it to a folder and double-click the EXE to run. Windows Explorer should show the embedded icon for the EXE file.
- Create a desktop shortcut (the script attempts this). Pinning to taskbar may require manual pinning; the running app should show the embedded icon on the taskbar.

Limitations & caveats
- Building on Linux/macOS will not produce a proper Windows EXE. Use a Windows build host or Windows CI runner.
- Even with icon embedded, Windows may cache icons; if you replaced an existing exe, clear the icon cache or reboot to refresh.
- Code signing requires a valid certificate and access to `signtool.exe`.
