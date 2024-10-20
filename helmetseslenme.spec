# -*- mode: python ; coding: utf-8 -*-
import sys
sys.setrecursionlimit(sys.getrecursionlimit() + 12525)

a = Analysis(
    ['helmetseslenme.py'],
    pathex=[],
    binaries=[],
    datas=[("C:\\Users\\Yigit\\AppData\\Local\\Programs\\Python\\Python311\\Lib\\site-packages\\ultralytics\\cfg\\default.yaml", "ultralytics\\cfg"),("C:\\Users\\Yigit\\Desktop\\PyTorchDemos\\PyTorchDemos\\issagligi\\helmet.pt",".")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='helmetseslenme',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
