"""Build helper for CriderGPT Offline for Windows.

This script prepares the frontend build (Vite) and the backend packaging steps
and generates the exact PyInstaller command you should run on a Windows machine
to produce a single-file executable. It will try to run frontend build locally
if Node is available. It will not run PyInstaller automatically unless executed
on Windows and `--pyinstaller` is passed.

Usage (recommended on Windows):
  python tools/build_windows.py --prepare --pyinstaller --icon offline_ui/public/cridergpt.ico --version 1.0

Usage (to prepare frontend bundle on current machine):
  python tools/build_windows.py --prepare

This script is safe to run locally and is intended to be run by Jessie on a dev
machine or CI runner that targets Windows. It writes a /build/ folder with the
prepared payload and a `pyinstaller_cmd.txt` file containing the exact command
to run on Windows.
"""
from __future__ import annotations
import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OFFLINE_UI = ROOT / "offline_ui"
BUILD_DIR = ROOT / "build" / "cridergpt_app"
DIST_DIR = OFFLINE_UI / "dist"


def check_dirs():
    present = {}
    for d in ["core", "backend", "ui", "models", "runtime_cache", "shadow", "data", "brain"]:
        p = ROOT / d
        present[d] = p.exists()
    return present


def run_frontend_build():
    if not OFFLINE_UI.exists():
        print("Frontend folder offline_ui/ not found. Skipping frontend build.")
        return False
    # run npm install if node_modules missing
    if not (OFFLINE_UI / "node_modules").exists():
        print("node_modules not found in offline_ui. Running npm install (this may take a while)...")
        subprocess.check_call(["npm", "install"], cwd=str(OFFLINE_UI))
    print("Running npm run build in offline_ui...")
    subprocess.check_call(["npm", "run", "build"], cwd=str(OFFLINE_UI))
    return True


def prepare_build_tree():
    # clear build dir
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    # copy backend files (all .py files and templates)
    backend_dst = BUILD_DIR / "backend"
    backend_dst.mkdir()
    for p in ROOT.glob("*.py"):
        shutil.copy2(p, backend_dst / p.name)
    # copy agent and other scripts
    for d in ["agent", "offline_logs", "shadow"]:
        src = ROOT / d
        if src.exists():
            dst = BUILD_DIR / d
            shutil.copytree(src, dst)
    # copy frontend dist if exists
    if DIST_DIR.exists():
        shutil.copytree(DIST_DIR, BUILD_DIR / "www")
    else:
        print("Warning: frontend dist not found; build will include no static UI. Run frontend build first.")


def generate_pyinstaller_command(icon: str | None, version: str):
    # PyInstaller command template for Windows
    exe_name = f"CriderGPT_Offline_v{version}.exe"
    cmd = [
        "pyinstaller",
        "--onefile",
        "--noconsole",
        f"--name={exe_name}",
        f"--add-data=www;www",
        f"--add-data=agent;agent",
        f"--add-data=offline_logs;offline_logs",
        f"--add-data=shadow;shadow",
    ]
    if icon:
        cmd.append(f"--icon={icon}")
    cmd.append(str(ROOT / "main.py"))
    # return a string that is safe to paste in Windows cmd (with escapes shown)
    return " \\\n+".join(cmd)


def write_pyinstaller_cmd(cmd: str):
    out = BUILD_DIR / "pyinstaller_cmd.txt"
    out.write_text(cmd)
    print(f"Wrote PyInstaller command template to {out}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prepare", action="store_true", help="Prepare build folder and frontend dist")
    parser.add_argument("--pyinstaller", action="store_true", help="Run pyinstaller when on Windows")
    parser.add_argument("--icon", help="Path to .ico to embed into exe (relative to repo root)")
    parser.add_argument("--version", default="1.0", help="Version string to embed into exe name")
    args = parser.parse_args()

    print("Checking required directories...")
    present = check_dirs()
    for k, v in present.items():
        print(f"  {k}: {'FOUND' if v else 'MISSING'}")

    if args.prepare:
        # run frontend build if possible
        try:
            run_frontend_build()
        except Exception as e:
            print("Frontend build failed:", e)
        prepare_build_tree()
        cmd = generate_pyinstaller_command(args.icon, args.version)
        write_pyinstaller_cmd(cmd)

    if args.pyinstaller:
        if platform.system() != "Windows":
            print("PyInstaller step must run on Windows. Generated command is in build/cridergpt_app/pyinstaller_cmd.txt")
        else:
            # run pyinstaller
            try:
                print("Running PyInstaller (this will create dist/ and build/pyinstaller folders)...")
                py_cmd = [
                    "pyinstaller",
                    "--onefile",
                    "--noconsole",
                    f"--name=CriderGPT_Offline_v{args.version}.exe",
                ]
                if args.icon:
                    py_cmd.append(f"--icon={args.icon}")
                # add data pieces (PyInstaller expects ; on Windows; this call is executed on Windows)
                py_cmd += [
                    "--add-data",
                    f"{str(BUILD_DIR / 'www')};www",
                    "--add-data",
                    f"{str(BUILD_DIR / 'agent')};agent",
                ]
                py_cmd.append(str(ROOT / "main.py"))
                subprocess.check_call(py_cmd)
                print("PyInstaller finished. Move the exe from dist/ to build/cridergpt_app/")
            except Exception as e:
                print("PyInstaller failed:", e)


if __name__ == "__main__":
    main()
