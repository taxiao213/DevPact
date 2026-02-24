# -*- mode: python ; coding: utf-8 -*-
import sys
import os

block_cipher = None

hidden_imports = [
    'langgraph',
    'langgraph.graph',
    'langgraph.pregel',
    'langgraph.channels',
    'langgraph.func',
    'langchain',
    'langchain_core',
    'langchain_core.messages',
    'langchain_core.prompts',
    'langchain_core.output_parsers',
    'langchain_openai',
    'langchain_openai.chat_models',
    'pydantic',
    'pydantic.v1',
    'openai',
    'httpx',
    'httpcore',
    'anyio',
    'anyio._backends._asyncio',
    'sniffio',
    'h11',
    'certifi',
    'idna',
    'charset_normalizer',
    'dotenv',
    'jsonpatch',
    'jsonpointer',
    'tenacity',
    'distro',
    'jiter',
    'tqdm',
    'langsmith',
    'yaml',
    'annotated_types',
    'PIL',
    'PIL.Image',
    'numpy',
    'tiktoken',
    'regex',
    'packaging',
    'typing_extensions',
]

collect_packages = [
    'langgraph',
    'langchain',
    'langchain_openai',
    'langchain_core',
    'pydantic',
    'openai',
]

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

datas = [
    ('state.py', '.'),
    ('agents.py', '.'),
    ('discussion.py', '.'),
    ('code_reader.py', '.'),
]

binaries = []
all_hiddenimports = hidden_imports.copy()

for pkg in collect_packages:
    try:
        datas.extend(collect_data_files(pkg))
    except Exception:
        pass
    try:
        all_hiddenimports.extend(collect_submodules(pkg))
    except Exception:
        pass
    try:
        binaries.extend(collect_dynamic_libs(pkg))
    except Exception:
        pass

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=all_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='DevPact',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='DevPact',
)

if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='DevPact.app',
        icon=None,
        bundle_identifier='app.devpact.main',
        info_plist={
            'CFBundleName': 'DevPact',
            'CFBundleDisplayName': 'DevPact',
            'CFBundleVersion': '1.0.0',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleIdentifier': 'app.devpact.main',
            'NSHighResolutionCapable': True,
            'LSMinimumSystemVersion': '10.13.0',
        },
    )
