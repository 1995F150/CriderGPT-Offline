"""Agent CLI: verify protected paths, log actions, and provide advisory deny for protected edits.

This is an in-repo, auditable tool. It does not change OS permissions by itself.
"""
import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from typing import Dict

LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "offline_logs", "agent.log")
MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "core_manifest.json")
KEYS_PATH = os.path.join(os.path.dirname(__file__), "keys.json")


def _log(line: str) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    ts = datetime.utcnow().isoformat() + "Z"
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{ts} {line}\n")


def load_manifest() -> Dict[str, str]:
    if not os.path.exists(MANIFEST_PATH):
        return {}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def verify_manifest() -> None:
    manifest = load_manifest()
    mismatches = []
    missing = []
    for path, saved_hash in manifest.items():
        if not os.path.exists(path):
            missing.append(path)
            continue
        h = hashlib.sha256()
        try:
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    h.update(chunk)
            if h.hexdigest() != saved_hash:
                mismatches.append(path)
        except Exception as e:
            mismatches.append(path)
    print(f"Manifest entries: {len(manifest)}")
    print(f"Missing: {len(missing)}")
    print(f"Mismatched: {len(mismatches)}")
    if missing or mismatches:
        _log(f"verify FAILED: missing={len(missing)} mismatched={len(mismatches)}")
    else:
        _log("verify OK")


def show_manifest():
    manifest = load_manifest()
    for p in sorted(manifest.keys()):
        print(p)


def require_override(key: str) -> bool:
    # Advisory: compare SHA256 of provided key to stored hash
    if not os.path.exists(KEYS_PATH):
        print("No keys configured. Abort.")
        return False
    with open(KEYS_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    stored = data.get("override_key_hash")
    if not stored:
        print("No override key set in keys.json")
        return False
    hk = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return hk == stored


def main():
    parser = argparse.ArgumentParser(description="CriderGPT agent helper")
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("verify", help="Verify manifest checksums for tracked files")
    sub.add_parser("show", help="Show manifest paths")
    erase = sub.add_parser("erase", help="Advisory: Erase path (requires override)")
    erase.add_argument("path")
    args = parser.parse_args()
    if args.cmd == "verify":
        verify_manifest()
        return
    if args.cmd == "show":
        show_manifest()
        return
    if args.cmd == "erase":
        # Advisory-only: require override key
        k = input("Enter override key: ")
        if not require_override(k):
            print("Override key invalid. Action denied.")
            _log(f"unauthorized erase attempt: {args.path}")
            sys.exit(1)
        # If valid, perform the destructive operation after confirmation
        confirm = input(f"CONFIRM erase {args.path}? Type YES to proceed: ")
        if confirm == "YES":
            try:
                if os.path.isdir(args.path):
                    import shutil

                    shutil.rmtree(args.path)
                else:
                    os.remove(args.path)
                print("Erased")
                _log(f"erase OK: {args.path}")
            except Exception as e:
                print("Failed to erase:", e)
                _log(f"erase FAIL: {args.path} {e}")
        else:
            print("Cancelled")
            _log(f"erase cancelled: {args.path}")


if __name__ == "__main__":
    main()
