#!/usr/bin/env python3
from PyQt6.QtCore import QSettings
import os

print("=== Deep QSettings Analysis ===")

# Check global domain
s_global = QSettings(QSettings.Scope.UserScope, QSettings.Format.NativeFormat)
print(f'Global settings fileName: {s_global.fileName()}')
print(f'Global settings allKeys count: {len(s_global.allKeys())}')
print()

# Check if our keys are in global domain
our_keys = ['api_key', 'frontend_path', 'backend_path', 'language', 'model', 'max_rounds', 'base_url']
for key in our_keys:
    if s_global.contains(key):
        print(f'Found in global: {key} = {s_global.value(key)}')

print()

# Check the actual QSettings we use
s = QSettings('MultiAgentDev', 'MultiAgentDev')
print(f'App settings fileName: {s.fileName()}')
print(f'App settings format: {s.format()}')
print(f'App settings scope: {s.scope()}')
print(f'File exists: {os.path.exists(s.fileName())}')
print()

# Check all keys
print('All keys in app settings:')
for key in s.allKeys():
    if key in our_keys:
        print(f'  {key}: {s.value(key)}')

print()

# Try to sync and check if file is created
s.sync()
print(f'After sync, file exists: {os.path.exists(s.fileName())}')

# Check if the plist directory exists
plist_dir = os.path.dirname(s.fileName())
print(f'plist dir exists: {os.path.exists(plist_dir)}')
print(f'plist dir: {plist_dir}')

# List files in plist dir
if os.path.exists(plist_dir):
    files = [f for f in os.listdir(plist_dir) if 'multi' in f.lower() or 'agent' in f.lower()]
    print(f'Related files in dir: {files}')
