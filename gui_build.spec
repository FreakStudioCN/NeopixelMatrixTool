# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

a = Analysis(
    ['gui_app.py'],  # 主程序文件
    pathex=[],
    binaries=[],
    datas=[('assets/*.png', 'assets'), ('assets/*.jpg', 'assets')],
    hiddenimports=[
        'pygame',
        'cv2',
        'PIL',
        'numpy',
        'tkinter',
        'pillow',
        'argparse',
        'natsort',
        'tqdm'
    ],  # 确保模块名没有遗漏
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes = [
    'matplotlib', 'scipy', 'pandas',
    'tkinter.test', 'test', 'unittest'],
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
    name='NeopixelMatrixTool v1.0 by Freak嵌入式',  # 可执行文件的名称
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 如果是命令行程序，保持 console=True
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NeopixelMatrixTool.ico'
)
