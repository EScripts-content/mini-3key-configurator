# -*- mode: python ; coding: utf-8 -*-
import os
import importlib.util
from PyInstaller.utils.hooks import collect_all

pynput_datas, pynput_binaries, pynput_hiddenimports = collect_all('pynput')

# Detectar pywinusb dinamicamente (sin paths personales hardcodeados)
# Usar %APPDATA% para path portable sin revelar nombre de usuario
pywinusb_data = None
pywinusb_dir = os.path.expandvars(r'%APPDATA%\Python\Python314\site-packages\pywinusb')
if os.path.isdir(pywinusb_dir):
    pywinusb_data = (pywinusb_dir, 'pywinusb')

# Construir lista de datas
all_datas = [
    ('assets', 'assets'),
    ('presets', 'presets'),
]
all_datas.extend(pynput_datas)
if pywinusb_data:
    all_datas.append(pywinusb_data)

# pathex para que PyInstaller encuentre pywinusb durante el analisis
user_site = os.path.expandvars(r'%APPDATA%\Python\Python314\site-packages')

a = Analysis(
    ['main.py'],
    pathex=[user_site],
    binaries=[*pynput_binaries],
    datas=all_datas,
    hiddenimports=[
        'pywinusb',
        'pywinusb.hid',
        'pynput',
        'pynput.keyboard',
        'pynput.keyboard._win32',
        'pynput.mouse',
        'pynput.mouse._win32',
        'pynput._util',
        'pynput._util.win32',
        'six',
        'win32api',
        'win32con',
        'win32gui',
        'ctypes',
        'ctypes.wintypes',
        *pynput_hiddenimports,
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['Xlib', 'AppKit', 'Quartz', 'CoreFoundation', 'evdev'],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='MiniConfigurator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    icon=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='MiniConfigurator',
)
