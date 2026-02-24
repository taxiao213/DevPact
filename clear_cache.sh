#!/bin/bash

echo "=========================================="
echo "DevPact - Clear Cache & Settings"
echo "=========================================="
echo ""

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Clearing QSettings from Global Domain..."
    
    defaults delete -g api_key 2>/dev/null && echo "  ✓ Removed api_key"
    defaults delete -g frontend_path 2>/dev/null && echo "  ✓ Removed frontend_path"
    defaults delete -g backend_path 2>/dev/null && echo "  ✓ Removed backend_path"
    defaults delete -g language 2>/dev/null && echo "  ✓ Removed language"
    defaults delete -g model 2>/dev/null && echo "  ✓ Removed model"
    defaults delete -g max_rounds 2>/dev/null && echo "  ✓ Removed max_rounds"
    defaults delete -g base_url 2>/dev/null && echo "  ✓ Removed base_url"
    
    echo ""
    echo "Removing configuration files..."
    
    rm -rf "$HOME/.config/MultiAgentDev" 2>/dev/null && echo "  ✓ Removed ~/.config/MultiAgentDev (INI settings)"
    
    rm -rf "$HOME/Library/Application Support/MultiAgentDev/MultiAgentDev.ini" 2>/dev/null
    rm -rf "$HOME/Library/Application Support/MultiAgentDev" 2>/dev/null && echo "  ✓ Removed Application Support folder"
    
    rm -rf "$HOME/Library/Preferences/com.multiagentdev.MultiAgentDev.plist" 2>/dev/null && echo "  ✓ Removed preferences plist (com.multiagentdev)"
    
    rm -rf "$HOME/Library/Preferences/app.devpact.main.plist" 2>/dev/null && echo "  ✓ Removed preferences plist (app.devpact.main)"
    
    rm -rf "$HOME/Library/Caches/MultiAgentDev" 2>/dev/null && echo "  ✓ Removed cache directory"
    
    rm -rf "$HOME/Library/HTTPStorages/app.devpact.main" 2>/dev/null
    rm -rf "$HOME/Library/Saved Application State/app.devpact.main.savedState" 2>/dev/null && echo "  ✓ Removed saved state"
fi

echo ""
echo "Cleaning build artifacts..."

rm -rf build dist *.spec icon.iconset icon.icns __pycache__ .pytest_cache
rm -rf state/__pycache__ agents/__pycache__ discussion/__pycache__ code_reader/__pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
rm -rf .ruff_cache .mypy_cache 2>/dev/null

echo "  ✓ Build artifacts cleaned"

echo ""
echo "=========================================="
echo "✅ Cache and settings cleared!"
echo "=========================================="
