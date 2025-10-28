"""Runtime initializer for CriderGPT Offline.

This script performs a safe, offline 'initialization' step:
- prints the activation message
- loads version metadata and manifest
- verifies checksums for protected core files
- writes an entry to offline_logs/agent.log
- offers advisory routines to set OS-level immutability (prints commands, does not run privileged ops)

Run this at startup manually to simulate system initialization. It does NOT
change system-level protections by itself.
"""
import hashlib
import json
import os
import stat
import sys
from datetime import datetime

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
LOG_PATH = os.path.join(ROOT, 'offline_logs', 'agent.log')
MANIFEST_PATH = os.path.join(ROOT, 'agent', 'core_manifest.json')
VERSION_META = os.path.join(ROOT, 'tools', 'version_metadata.json')


def log(line: str) -> None:
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    ts = datetime.utcnow().isoformat() + 'Z'
    with open(LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"{ts} {line}\n")


def sha256_of_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def verify_manifest() -> dict:
    if not os.path.exists(MANIFEST_PATH):
        log('runtime_init: manifest missing')
        return {'status': 'no-manifest', 'checked': 0}
    with open(MANIFEST_PATH, 'r', encoding='utf-8') as f:
        manifest = json.load(f)
    mismatched = []
    missing = []
    checked = 0
    for p, h in manifest.items():
        checked += 1
        if not os.path.exists(p):
            missing.append(p)
            continue
        try:
            cur = sha256_of_file(p)
            if cur != h:
                mismatched.append(p)
        except Exception:
            mismatched.append(p)
    status = {'status': 'ok' if not (missing or mismatched) else 'fail', 'checked': checked, 'missing': missing, 'mismatched': mismatched}
    log(f"runtime_init: verify manifest result: {status['status']} checked={checked} missing={len(missing)} mismatched={len(mismatched)}")
    return status


def load_version_meta():
    if not os.path.exists(VERSION_META):
        return {}
    with open(VERSION_META, 'r', encoding='utf-8') as f:
        return json.load(f)


def set_readonly(path: str) -> None:
    """Make a file read-only (advisory). For real immutability, run chattr or OS ACLs."""
    try:
        current = os.stat(path)
        os.chmod(path, current.st_mode & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
        log(f"runtime_init: set readonly {path}")
    except Exception as e:
        log(f"runtime_init: failed set readonly {path} - {e}")


def advisory_chattr_commands(paths):
    """Return commands the admin can run to set immutable flags on Linux."""
    cmds = []
    for p in paths:
        cmds.append(f"sudo chattr +i {p}")
    return cmds


def main():
    # Activation message
    print('CriderGPT Core Activated — Offline Brain Online.')
    log('runtime_init: activation')

    # Load and show version metadata
    meta = load_version_meta()
    if meta:
        print(f"Product: {meta.get('ProductName','CriderGPT')} - {meta.get('FileDescription','Offline AI Assistant')}")
    else:
        print('Version metadata not found.')

    # Verify manifest
    v = verify_manifest()
    if v.get('status') != 'ok':
        print('⚠️ SYSTEM ALERT: Protected Core File — Unauthorized Edit Rejected.')
        if v.get('missing'):
            print('Missing files:', *v.get('missing'))
        if v.get('mismatched'):
            print('Mismatched files:', *v.get('mismatched'))
    else:
        print('All protected files verified OK.')

    # Advisory locking suggestion
    print('\nAdvisory: to harden core files, run the following commands as root on Linux:')
    protected_paths = [
        os.path.join(ROOT, 'setup.py'),
        os.path.join(ROOT, 'main.py'),
        os.path.join(ROOT, 'tools', 'version_metadata.json'),
        os.path.join(ROOT, 'offline_ui', 'src', 'components', 'ChatInterface.tsx'),
        os.path.join(ROOT, 'offline_ui', 'src', 'components', 'AIAssistant.tsx'),
        os.path.join(ROOT, 'offline_ui', 'src', 'components', 'navigation-menu.tsx'),
        os.path.join(ROOT, 'offline_ui', 'src', 'components', 'command.tsx'),
    ]
    cmds = advisory_chattr_commands(protected_paths)
    for c in cmds:
        print('  ', c)

    print('\nNote: This initialization is advisory. To enforce immutability you must run OS-level commands or configure ACLs. Logs written to', LOG_PATH)


if __name__ == '__main__':
    main()
