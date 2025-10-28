# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for CriderGPT Offline.

This spec bundles the main.py entrypoint, includes the prepared 'www' frontend folder
and auxiliary folders, and sets the application icon. For version metadata we recommend
using the post-build `tools/build_windows_post.ps1` which uses rcedit to embed the full
version strings (CompanyName, ProductName, etc.).

To build on Windows with this spec:
  pyinstaller tools\cridergpt.spec

"""
import os
from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

ROOT = os.path.abspath(os.path.join(__file__, '..'))

datas = []
def add_data(src, dest):
    srcp = os.path.join(ROOT, src)
    if os.path.exists(srcp):
        datas.append((srcp, dest))

# include frontend www, agent scripts, logs and shadow
add_data('build\\cridergpt_app\\www', 'www')
add_data('build\\cridergpt_app\\agent', 'agent')
add_data('build\\cridergpt_app\\offline_logs', 'offline_logs')
add_data('build\\cridergpt_app\\shadow', 'shadow')

icon_file = os.path.join(ROOT, 'offline_ui', 'public', 'cridergpt.ico')

a = Analysis([
    os.path.join(ROOT, 'main.py')],
             pathex=[ROOT],
             binaries=[],
             datas=datas,
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='CriderGPT_Offline_v1.0',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          icon=icon_file)

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='CriderGPT_Offline_v1.0')
