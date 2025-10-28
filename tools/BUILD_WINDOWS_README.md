# Building CriderGPT Offline executable for Windows

This document explains how to produce a single-file Windows executable (.exe)
from the repository contents. The repository contains a helper script
`tools/build_windows.py` that prepares the payload and produces an exact
PyInstaller command you can run on a Windows build host.

Important: This repo does NOT automatically produce an .exe inside this Linux
devcontainer. Use a Windows machine (or Windows CI) with Python and Node.js
installed to produce the final executable.

Prerequisites (on Windows machine):
- Python 3.10+ (same major line used for development)
- pip install pyinstaller
- Node.js (for building the frontend)
- npm install in `offline_ui`

High-level steps
1. On your Windows build machine, clone this repo or copy the repository contents.
2. Prepare the frontend and build payload (from repo root):

```powershell
python tools\build_windows.py --prepare --version 1.0 --icon offline_ui\public\cridergpt.ico
```

This will:
- run `npm install` (if needed) and `npm run build` inside `offline_ui` to create `offline_ui/dist`;
- copy backend Python files, `agent/`, `offline_logs/`, `shadow/` and the `www` frontend bundle into `build\cridergpt_app`;
- write a `pyinstaller_cmd.txt` file inside `build\cridergpt_app` with the exact PyInstaller command to run.

3. Run PyInstaller using the generated command (copy-paste from `pyinstaller_cmd.txt`) or use the prepared command below.

Example PyInstaller command (run from repo root on Windows cmd.exe):

```cmd
pyinstaller --onefile --noconsole --name=CriderGPT_Offline_v1.0 --add-data build\cridergpt_app\www;www --add-data build\cridergpt_app\agent;agent --add-data build\cridergpt_app\offline_logs;offline_logs --add-data build\cridergpt_app\shadow;shadow --icon offline_ui\public\cridergpt.ico main.py
```

Notes about `--add-data` paths:
- On Windows the syntax is `SOURCE;DEST` when passed to PyInstaller.
- The `main.py` script in the repository serves static files from `offline_ui/dist` when present; PyInstaller bundles the `www` folder and the app expects to find it next to the binary.

4. Move the produced exe into the build payload folder:

```cmd
move dist\CriderGPT_Offline_v1.0.exe build\cridergpt_app\CriderGPT_Offline_v1.0.exe
```

5. Post-build verification (on Windows)
- Run the built EXE silently to ensure it starts the Flask server and can serve static UI.
- Generate checksums:

```cmd
certutil -hashfile build\cridergpt_app\CriderGPT_Offline_v1.0.exe SHA256 > build\verify.log
```

6. Hardening: make core data read-only
- Inside the binary this is not trivially changeable, but ensure any external directories you ship alongside the exe (shadow, agent, models) are flagged as read-only via file permissions and documentation.

Security and limitations
- This process bundles Python sources inside the executable; truly preventing runtime code inspection is not feasible—use OS-level protections and signed binaries to increase integrity.
- This helper does not sign the binary. To sign the exe with an Authenticode certificate, use Microsoft's `signtool` on Windows after building.

If you want, I can also:
- Add a PyInstaller spec template file.
- Create a small PowerShell script that runs the build end-to-end on a Windows host.
