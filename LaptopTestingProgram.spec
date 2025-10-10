# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\Programming\\program exercise\\Python\\auto test\\script.py'],
    pathex=[],
    binaries=[],
    datas=[('icon.png', '.'), ('icon.ico', '.'), ('requirements.txt', '.'), ('README.md', '.')],
    hiddenimports=['hardware_info', 'os_info', 'system_tests', 'update_manager', 'window_utils', 'subprocess_helper', 'PySide6.QtCore', 'PySide6.QtGui', 'PySide6.QtWidgets'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5', 'PyQt6', 'tkinter', 'kivy', 'kivymd'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LaptopTestingProgram',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['D:\\Programming\\program exercise\\Python\\auto test\\icon.ico'],
)
