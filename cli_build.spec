# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(
    ['cli_app.py'],  # 修改主程序入口
    pathex=[],
    binaries=[],
    datas=[
        ('assets/*.png', 'assets'),
        ('assets/*.jpg', 'assets')
    ],
    hiddenimports=[
        'pygame',
        'cv2',
        'PIL',
        'numpy',
        'argparse',  # CLI必需
        'natsort',
        'tqdm'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',  # CLI不需要GUI相关库
        'matplotlib',
        'scipy',
        'pandas',
        'tkinter.test',
        'test',
        'unittest'
    ],
    noarchive=False,
    optimize=0,
    icon='NeopixelMatrixTool.ico'  # 保留图标
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NeopixelMatrixTool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # 必须为True（命令行程序）
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NeopixelMatrixTool.ico'
)