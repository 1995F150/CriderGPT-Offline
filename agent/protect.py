"""Simple protection utilities: compute and save file checksums (SHA256).

Usage:
  python -m agent.protect --paths path1 path2 --out agent/core_manifest.json

This module is intentionally minimal and designed to be run locally by Jessie.
"""
import hashlib
import json
import os
from typing import Dict, List


def sha256_of_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def build_manifest(paths: List[str]) -> Dict[str, str]:
    manifest: Dict[str, str] = {}
    for p in paths:
        if os.path.isfile(p):
            manifest[p] = sha256_of_file(p)
        elif os.path.isdir(p):
            for root, _, files in os.walk(p):
                for fn in files:
                    full = os.path.join(root, fn)
                    try:
                        manifest[full] = sha256_of_file(full)
                    except Exception:
                        # skip unreadable files
                        continue
        else:
            # path doesn't exist; skip
            continue
    return manifest


def save_manifest(manifest: Dict[str, str], out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Compute checksums for paths and save manifest")
    parser.add_argument("--paths", nargs="+", help="Paths to include", required=True)
    parser.add_argument("--out", help="Output manifest JSON path", required=True)
    args = parser.parse_args()
    m = build_manifest(args.paths)
    save_manifest(m, args.out)
    print(f"Wrote manifest with {len(m)} entries to {args.out}")
