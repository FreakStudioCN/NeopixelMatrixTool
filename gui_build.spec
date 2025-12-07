# -*- mode: python ; coding: utf-8 -*-
import os
import glob
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

# ---- 核心配置：手动指定项目根目录（解决__file__未定义问题） ----
project_dir = r'G:\NeopixelMatrixTool'  # 直接写死项目路径，避免__file__依赖
pathex = [project_dir]

# ---------------- 1. 资源文件收集（assets + PIL + 字体） ----------------
# 收集assets目录所有文件（递归，保留目录结构）
datas = []
assets_dir = os.path.join(project_dir, 'assets')
if os.path.isdir(assets_dir):
    for root, _, files in os.walk(assets_dir):
        for file in files:
            src_path = os.path.join(root, file)
            # 计算相对路径，保证dist里的assets目录结构和源码一致
            rel_dir = os.path.relpath(root, assets_dir)
            dest_path = os.path.join('assets', rel_dir)
            datas.append((src_path, dest_path))

# 收集PIL的静态资源（字体/配置等）
datas += collect_data_files('PIL')

# 收集pygame的资源文件（含SDL3相关配置）
datas += collect_data_files('pygame')

# ---------------- 2. 二进制文件收集（重点处理SDL2/SDL3 DLL） ----------------
binaries = []

# ① 收集pygame依赖的所有动态库（自动识别SDL2/SDL3）
binaries += collect_dynamic_libs('pygame')

# ② 手动补充Conda环境下的SDL DLL（优先级高于自动收集）
conda_env_dir = r'G:\miniconda\install\envs\PyQtDev'  # 手动指定Conda环境路径
sdl_dll_paths = [
    os.path.join(conda_env_dir, 'Library', 'bin', 'SDL2.dll'),
    os.path.join(conda_env_dir, 'Library', 'bin', 'SDL2_image.dll'),
    os.path.join(conda_env_dir, 'Library', 'bin', 'SDL2_mixer.dll'),
    os.path.join(conda_env_dir, 'Library', 'bin', 'SDL2_ttf.dll'),
    os.path.join(conda_env_dir, 'Library', 'bin', 'SDL3.dll'),  # SDL3重点处理
]
for dll_path in sdl_dll_paths:
    if os.path.exists(dll_path):
        binaries.append((dll_path, '.'))  # 放到exe同级目录，确保pygame能找到

# ③ 兜底：从系统路径/虚拟环境收集SDL3
if sys.platform == 'win32':
    # 检查Python环境的DLL目录
    python_dll_dir = os.path.join(sys.prefix, 'DLLs')
    for sdl_dll in ['SDL3.dll', 'SDL2.dll']:
        dll_path = os.path.join(python_dll_dir, sdl_dll)
        if os.path.exists(dll_path):
            binaries.append((dll_path, '.'))

# 去重：避免重复打包相同DLL
seen_bin = set()
unique_binaries = []
for src, tgt in binaries:
    norm_src = os.path.normcase(os.path.abspath(src))
    if norm_src not in seen_bin:
        seen_bin.add(norm_src)
        unique_binaries.append((src, tgt))
binaries = unique_binaries

# ---------------- 3. 隐藏导入（解决SDL3/pygame/tkinter动态导入问题） ----------------
hiddenimports = [
    # 核心依赖
    'pygame',
    'pygame.sdl3',  # 显式导入SDL3模块
    'pygame.sdl3.video',
    'pygame.sdl3.audio',
    'cv2',
    'numpy',
    'natsort',
    'tqdm',
    'tkinter',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'PIL',
    'PIL.ImageTk',
    # 项目子模块
] + collect_submodules('ws_converter')  # 自动收集ws_converter所有子模块

# ---------------- 4. 主打包配置（OneDir模式核心） ----------------
a = Analysis(
    ['gui_app.py'],  # 主程序入口
    pathex=pathex,
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    # 排除无关库，减小体积
    excludes=[
        'matplotlib', 'scipy', 'pandas',
        'tkinter.test', 'test', 'unittest',
        'jupyter', 'ipython', 'notebook'
    ],
    noarchive=False,
    optimize=0,  # 调试阶段关闭优化，便于排查问题
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    optimize=0,
)

# ---------------- 5. OneDir模式：生成独立目录（核心修改） ----------------
# EXE部分：仅生成引导程序，不包含二进制文件
exe = EXE(
    pyz,
    a.scripts,
    [],  # 空列表表示不嵌入binaries（onedir模式）
    exclude_binaries=True,  # 关键：onedir模式必须设为True
    name='NeopixelMatrixTool_v1.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,  # onedir模式建议关闭UPX，避免DLL冲突
    console=True,  # 调试阶段保留控制台，发布时可改为False
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    icon=os.path.join(project_dir, 'NeopixelMatrixTool.ico'),  # 图标路径
)

# COLLECT部分：将所有依赖打包到独立目录（onedir核心）
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    name='NeopixelMatrixTool_v1.0',  # 最终生成的目录名
)