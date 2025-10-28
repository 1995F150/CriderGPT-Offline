# CriderGPT Offline

Offline AI desktop app scaffold (Flask backend + React + TypeScript + Vite + Tailwind frontend).

By Jessie Crider.

Quick start (development):

1. Create a Python virtual environment and install backend requirements:


# CriderGPT Offline

Offline AI desktop app scaffold (Flask backend + React + TypeScript + Vite + Tailwind frontend).

By Jessie Crider.

This README focuses on install, development, and packaging steps so you can run the project locally or prepare a Windows build.

## Quick start — Development (Linux / macOS / WSL)

1. Create and activate a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install backend Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install frontend dependencies (one-time):

```bash
cd offline_ui
npm install
cd ..
```

4. Run backend and frontend development servers in separate terminals:

Terminal A (backend):
```bash
source .venv/bin/activate
python main.py
```

Terminal B (frontend dev):
```bash
cd offline_ui
npm run dev
```

Open the UI at http://127.0.0.1:5000 (the Flask backend proxies the built frontend in production; Vite dev server runs on 5173).

## Production build (serve UI from Flask)

1. Build the frontend assets:

```bash
cd offline_ui
npm run build
cd ..
```

2. Start the Flask server (it will serve the built `offline_ui/dist` folder):

```bash
source .venv/bin/activate
python main.py
```

The app will be available at http://127.0.0.1:5000 serving static files from `offline_ui/dist`.

## Prepare a Windows single-file EXE (notes)

The repository contains helper tooling to prepare a Windows build, but final packaging must be done on Windows (PyInstaller and rcedit require Windows tooling).

High-level steps:

1. Ensure you have Node.js and Python (3.10+) on the Windows machine.
2. In the repo root, run the frontend build (`cd offline_ui && npm install && npm run build`).
3. On Linux we provide a prepare helper that copies `dist` into `build/cridergpt_app/www`:

```bash
python tools/build_windows.py --prepare --version 1.0 --icon offline_ui/public/cridergpt.ico
```

Note: The final PyInstaller run must be executed on Windows. Use the provided spec `tools/cridergpt.spec` and the post-build helper `tools/build_windows_post.ps1` to embed version metadata and optionally sign the executable.

Important packaging notes:
- Provide a valid multi-size `.ico` (16/32/48/256). Place it at `offline_ui/public/cridergpt.ico` before running prepare.
- PyInstaller single-file builds and Windows resource edits must run on Windows. See `tools/BUILD_WINDOWS_README.md` for a step-by-step Windows guide.

## Agent and integrity helpers

This repo includes an in-repo agent to help verify and protect key files:

- `agent/core_manifest.json` — manifest of protected files and their SHA256 hashes.
- `agent/keys.json` — stores a pre-shared override key (owner-managed).
- `agent/agent.py` — CLI for `verify`, `show`, and controlled `erase` operations.
- `agent/runtime_init.py` — runtime initializer that prints activation info, verifies the manifest, logs to `offline_logs/agent.log`, and prints advisory commands (e.g., `sudo chattr +i`) to make files immutable on Linux.

Usage examples:

```bash
python agent/agent.py verify    # verifies manifest and prints results
python agent/agent.py show      # prints the manifest entries
python agent/runtime_init.py    # run at startup to verify and log
```

If the manifest verification fails, the runtime will log the event to `offline_logs/agent.log` and print missing/mismatched files. For destructive actions the CLI enforces an override key.

## Troubleshooting

- Vite/PostCSS ESM error: If you see "module is not defined in ES module scope" during `npm run build`, ensure `offline_ui/postcss.config.cjs` exists (CommonJS) instead of `postcss.config.js` when `package.json` sets `type: "module"`.
- Missing `.ico` or bad icon: Convert your PNG/SVG to ICO with ImageMagick or an online converter. Example (on Linux with ImageMagick):

```bash
convert logo.png -resize 256x256 cridergpt.ico
```

- PyInstaller failures: Run the spec and post-processing on Windows; the provided `tools/build_windows_post.ps1` script automates rcedit and optional signing but requires Windows toolchain (rcedit, signtool).

## Useful commands (copy/paste)

Development (Linux/macOS):
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cd offline_ui && npm install
# in terminal A
python main.py
# in terminal B
cd offline_ui && npm run dev
```

Production (serve static UI from Flask):
```bash
cd offline_ui
npm run build
cd ..
source .venv/bin/activate
python main.py
```

Prepare Windows build (local helper):
```bash
cd offline_ui && npm run build
cd ..
python tools/build_windows.py --prepare --version 1.0 --icon offline_ui/public/cridergpt.ico
```

## Security & hardening recommendations

- Keep `agent/keys.json` in a secure location and rotate the override key offline when needed.
- Use `agent/runtime_init.py` at startup to detect unauthorized changes and log them to `offline_logs/agent.log`.
- To make files truly immutable on Linux, run the printed `sudo chattr +i <file>` commands (admin required). On Windows, apply strict ACLs and restrict write permissions to Administrators.

## License

MIT License © 2025 Jessie Crider (CriderGPT)

---

If you want, I can now:
- replace the placeholder `offline_ui/public/cridergpt.ico` with a provided ICO file (upload it or allow me to convert a source PNG/SVG),
- add a short `BUILD_WINDOWS_README.md` with exact Windows packaging steps,
- or add a tiny unit test for `agent/protect.py` to validate manifest generation.

Which of these would you like next?
