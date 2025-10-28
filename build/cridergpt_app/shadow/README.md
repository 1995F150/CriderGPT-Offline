# shadow snapshot placeholder

This folder is a placeholder for snapshot copies of protected core files.

Usage (manual):
- To restore a protected file from `shadow/`, copy the file from this directory back to its original location.
- This repo does not automatically create snapshots. Use `agent/protect.py` to generate checksums and create your own backups into `shadow/`.

Security note: Keep `shadow/` secure; treat it like a backup storage location. For stronger immutability, set filesystem-level protections (see `README_AGENT.md`).
