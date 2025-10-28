# CriderGPT Offline

Offline AI desktop app scaffold (Flask backend + React + TypeScript + Vite + Tailwind frontend).

By Jessie Crider.

Quick start (development):

1. Create a Python virtual environment and install backend requirements:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Start the Flask backend:

```bash
python main.py
```

3. In another terminal, start the frontend dev server:

```bash
cd offline_ui
npm install
npm run dev
```

Open http://127.0.0.1:5000 after building the frontend (`npm run build`) or open the Vite dev server directly (default 5173).

Notes and assumptions:
- Some exact uploaded component sources were not present in the prompt; I provided working React implementations consistent with your architecture.
- To serve the frontend from Flask, run `npm run build` in `offline_ui` to produce `offline_ui/dist`, then start `python main.py`.
# 🧠 CriderGPT Offline
### “Smarter Tech for Stronger Farms™”  
**Author:** Jessie Crider (CriderGPT)  
**Version:** v1.0.0 (Offline Prototype)

---

## 💡 Overview
CriderGPT Offline is a **standalone AI desktop application** that runs **without internet**, designed for modders, farmers, and creators.  
It mirrors the online version of CriderGPT but runs fully **locally** — like Blender or GIANTS Editor.  
You just open it and get to work — no browser, no connection, no limits.

---

## ⚙️ Core Features
- 🧠 **Offline AI Engine:** All logic and data stay stored on your computer.  
- 🧰 **FS Mod Tools:** Reads and validates `.xml`, `.i3d`, and `.zip` mod files.  
- 🪵 **Blender Bridge:** Supports 3D model automation for FS mods.  
- 💾 **Local Learning:** CriderGPT stores data over time and gets smarter the more you use it.  
- 🧮 **Offline Calculators:** Farming, welding, mechanical, and budget tools built-in.  
- 📁 **Project Sync:** Automatically keeps notes and logs per mod or map project.  

---

## 🧱 System Requirements
| Component | Minimum | Recommended |
|------------|----------|-------------|
| OS | Windows 10+ | Windows 11 / Linux |
| CPU | Dual-Core | Quad-Core or higher |
| RAM | 4 GB | 8–16 GB |
| Storage | 2 GB free | 10 GB (for learning data & textures) |
| GPU | Integrated | NVIDIA/AMD (for Blender/AI modules) |

---

## 🪜 Installation Guide
1. **Download the ZIP** (click the green `Code ▾ → Download ZIP` button).  
2. Extract it to a safe folder, for example:

C:\Users<YourName>\Documents\CriderGPT-Offline\

3. Launch **CriderGPT-Offline.exe**  
(If using prototype build: double-click `run.bat` or `app/start.py`)

If you’re using the Python source instead of the compiled EXE:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app/start.py


---

🧩 Folder Structure

CriderGPT-Offline/
├── app/                 # UI and program files
├── core/                # Offline AI engine
├── data/                # Mod samples and project files
├── models/              # Local training data and responses
├── logs/                # Project logs and CriderGPT notes
├── textures/            # Icons and interface textures
├── run.bat              # Quick launch file
└── README.md


---

🧠 How It Works

Local Engine: Handles responses, calculations, and data analysis.

Storage Layer: Saves your modding progress and project data automatically.

Learning System: Improves results using your stored data and file history.

Blender/GIANTS Link: Integrates with 3D or map tools directly from your desktop.


Everything runs offline, entirely from your machine.
No cloud sync, no telemetry, and no internet dependencies.


---

🧾 License

MIT License © 2025 Jessie Crider (CriderGPT)
You may use, modify, and distribute freely with credit given.


---

🧱 Development Roadmap

[ ] CriderGPT File Doctor (mod structure checker)

[ ] Voice Assistant Mode

[ ] Local image recognition for texture scans

[ ] Auto XML Fixer

[ ] CriderGPT Model Trainer (learns from project data)

[ ] Offline update sync via USB



---

🧩 Credits

Built and maintained by
Jessie Crider — Founder of CriderGPT

> “Smarter Tech for Stronger Farms™”
