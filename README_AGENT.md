# CriderGPT Agent Toolkit

This small toolkit provides advisory, auditable scripts to compute and verify checksums for protected files, keep an action log, and require an override key for destructive actions.

Files added:
- `agent/protect.py` — compute SHA256 checksums for paths and write `agent/core_manifest.json`.
- `agent/agent.py` — CLI to verify manifest, show manifest, and perform an advisory erase that requires an override key.
- `agent/core_manifest.json` — manifest placeholder (JSON mapping path -> sha256).
- `agent/keys.json` — placeholder for override key hash (fill in with SHA256(secret)).
- `offline_logs/agent.log` — append-only log file created by scripts.
- `shadow/README.md` — guidance for manual snapshot/restore.

Quick start

1. Compute manifest for the directories you want protected (example protects `agent` and `core`):

```bash
python -m agent.protect --paths ./agent ./core --out ./agent/core_manifest.json
```

2. Verify the manifest:

```bash
python -m agent.agent verify
```

3. Show tracked paths:

```bash
python -m agent.agent show
```

4. To allow destructive operations via the agent CLI, set an override key:

```python
import hashlib
secret = "your-secret-string"
print(hashlib.sha256(secret.encode('utf-8')).hexdigest())
# Place the resulting hash into agent/keys.json as override_key_hash
```

Security and hardening (manual steps you should run locally if you want real immutability)

- Set file immutable flag on Linux:

```bash
sudo chattr +i path/to/protected/file_or_dir
```

- Use filesystem ACLs or OS-level permissions to restrict write access.
- Keep `shadow/` on a separate backup medium if possible.

Limitations

- These scripts are advisory within the repository. They do not automatically enforce OS-level protections.
- Anyone with filesystem access and the override key (or direct shell access) can still modify files. Use OS-level tools for strong protections.
