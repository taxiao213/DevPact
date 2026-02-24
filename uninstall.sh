#!/bin/bash

echo "=========================================="
echo "DevPact - Uninstall Script"
echo "=========================================="
echo ""

if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "This script is designed for macOS only."
    exit 1
fi

read -p "Are you sure you want to uninstall DevPact and remove all settings? (y/N): " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""
echo "Removing DevPact application..."

if [ -d "/Applications/DevPact.app" ]; then
    rm -rf "/Applications/DevPact.app"
    echo "  ✓ Removed /Applications/DevPact.app"
else
    echo "  - DevPact.app not found in /Applications"
fi

if [ -d "$HOME/Applications/DevPact.app" ]; then
    rm -rf "$HOME/Applications/DevPact.app"
    echo "  ✓ Removed ~/Applications/DevPact.app"
fi

echo ""
echo "Removing QSettings from Global Domain..."

defaults delete -g api_key 2>/dev/null && echo "  ✓ Removed api_key" || echo "  - api_key not found"
defaults delete -g frontend_path 2>/dev/null && echo "  ✓ Removed frontend_path" || echo "  - frontend_path not found"
defaults delete -g backend_path 2>/dev/null && echo "  ✓ Removed backend_path" || echo "  - backend_path not found"
defaults delete -g language 2>/dev/null && echo "  ✓ Removed language" || echo "  - language not found"
defaults delete -g model 2>/dev/null && echo "  ✓ Removed model" || echo "  - model not found"
defaults delete -g max_rounds 2>/dev/null && echo "  ✓ Removed max_rounds" || echo "  - max_rounds not found"
defaults delete -g base_url 2>/dev/null && echo "  ✓ Removed base_url" || echo "  - base_url not found"

echo ""
echo "Removing configuration files..."

if [ -d "$HOME/.config/MultiAgentDev" ]; then
    rm -rf "$HOME/.config/MultiAgentDev"
    echo "  ✓ Removed ~/.config/MultiAgentDev (INI settings)"
else
    echo "  - ~/.config/MultiAgentDev not found"
fi

if [ -d "$HOME/Library/Application Support/MultiAgentDev" ]; then
    rm -rf "$HOME/Library/Application Support/MultiAgentDev"
    echo "  ✓ Removed ~/Library/Application Support/MultiAgentDev"
else
    echo "  - ~/Library/Application Support/MultiAgentDev not found"
fi

if [ -f "$HOME/Library/Preferences/com.multiagentdev.MultiAgentDev.plist" ]; then
    rm -f "$HOME/Library/Preferences/com.multiagentdev.MultiAgentDev.plist"
    echo "  ✓ Removed preferences plist (com.multiagentdev)"
fi

if [ -f "$HOME/Library/Preferences/app.devpact.main.plist" ]; then
    rm -f "$HOME/Library/Preferences/app.devpact.main.plist"
    echo "  ✓ Removed preferences plist (app.devpact.main)"
fi

if [ -d "$HOME/Library/Caches/MultiAgentDev" ]; then
    rm -rf "$HOME/Library/Caches/MultiAgentDev"
    echo "  ✓ Removed cache directory"
else
    echo "  - Cache directory not found"
fi

if [ -d "$HOME/Library/HTTPStorages/app.devpact.main" ]; then
    rm -rf "$HOME/Library/HTTPStorages/app.devpact.main"
    echo "  ✓ Removed HTTP storage"
fi

if [ -d "$HOME/Library/Saved Application State/app.devpact.main.savedState" ]; then
    rm -rf "$HOME/Library/Saved Application State/app.devpact.main.savedState"
    echo "  ✓ Removed saved application state"
fi

echo ""
echo "Removing extended attributes (if any)..."

if [ -d "/Applications/DevPact.app" ]; then
    xattr -cr "/Applications/DevPact.app" 2>/dev/null
fi

echo ""
echo "=========================================="
echo "✅ DevPact has been completely uninstalled!"
echo "=========================================="
echo ""
echo "All settings and configuration files have been removed."
echo "You can reinstall DevPact at any time."
