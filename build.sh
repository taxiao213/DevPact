#!/bin/bash

echo "=========================================="
echo "DevPact - Build Script"
echo "=========================================="

echo ""
echo "Cleaning old build files..."
rm -rf build dist *.spec icon.iconset icon.icns __pycache__ .pytest_cache
rm -rf state/__pycache__ agents/__pycache__ discussion/__pycache__ code_reader/__pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null
rm -rf .ruff_cache .mypy_cache 2>/dev/null

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Clearing QSettings from Global Domain..."
    defaults delete -g api_key 2>/dev/null
    defaults delete -g frontend_path 2>/dev/null
    defaults delete -g backend_path 2>/dev/null
    defaults delete -g language 2>/dev/null
    defaults delete -g model 2>/dev/null
    defaults delete -g max_rounds 2>/dev/null
    defaults delete -g base_url 2>/dev/null
    echo "Global domain cleared!"
    
    # rm -rf ~/Library/Application\ Support/MultiAgentDev/MultiAgentDev.ini 2>/dev/null
    # rm -rf ~/Library/Preferences/com.multiagentdev.MultiAgentDev.plist 2>/dev/null
    rm -rf ~/Library/Application\ Support/MultiAgentDev 2>/dev/null
    rm -rf ~/Library/Caches/MultiAgentDev 2>/dev/null
fi

echo "Clean complete!"

PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found!"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"
$PYTHON_CMD --version

echo ""
echo "Installing dependencies..."
$PYTHON_CMD -m pip install pyinstaller PyQt6 langgraph langchain langchain-openai pydantic python-dotenv

echo ""
echo "Building executable..."
    
    # 使用完整路径的 pyinstaller
    PYINSTALLER_PATH="/Library/Frameworks/Python.framework/Versions/3.12/bin/pyinstaller"
    echo "Using pyinstaller: $PYINSTALLER_PATH"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Building for macOS..."
        
        ARCH=$(uname -m)
        echo "Architecture: $ARCH"
        
        echo "Creating app icon..."
        
        # 创建图标使用更安全的方式
        python3 << 'ICON_SCRIPT' 2>/dev/null || echo "Icon creation skipped"
import sys
import os

try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QPixmap, QPainter, QColor, QBrush, QPen, QFont
    from PyQt6.QtCore import Qt
    
    # 创建 QApplication（GUI 必需）
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    sizes = [16, 32, 64, 128, 256, 512]
    os.makedirs('icon.iconset', exist_ok=True)
    
    for size in sizes:
        pixmap = QPixmap(size, size)
        if pixmap.isNull():
            print(f"Failed to create pixmap for size {size}")
            continue
            
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor('#3B82F6')))
        painter.drawRoundedRect(0, 0, size, size, size // 4, size // 4)
        painter.setBrush(QBrush(QColor('white')))
        eye_size = size // 8
        eye_y = size // 3
        painter.drawEllipse(size // 3 - eye_size // 2, eye_y - eye_size // 2, eye_size, eye_size)
        painter.drawEllipse(2 * size // 3 - eye_size // 2, eye_y - eye_size // 2, eye_size, eye_size)
        mouth_y = 2 * size // 3
        mouth_width = size // 2
        mouth_height = size // 6
        painter.drawRoundedRect((size - mouth_width) // 2, mouth_y - mouth_height // 2, mouth_width, mouth_height, size // 10, size // 10)
        painter.end()
        pixmap.save(f'icon.iconset/icon_{size}x{size}.png')
        print(f"Created icon_{size}x{size}.png")
    
    # 使用 iconutil 创建 icns
    import subprocess
    result = subprocess.run(['iconutil', '-c', 'icns', 'icon.iconset'], capture_output=True, text=True)
    if result.returncode == 0:
        print('Icon created successfully')
    else:
        print(f'iconutil error: {result.stderr}')
        
except Exception as e:
    print(f"Icon creation failed: {e}")
    sys.exit(1)
ICON_SCRIPT
    
    ICON_ARG=""
    if [ -f "icon.icns" ]; then
        ICON_ARG="--icon icon.icns"
        echo "Using custom icon"
    else
        echo "No custom icon, using default"
    fi
    
    "$PYINSTALLER_PATH" --noconfirm --onefile --windowed \
        --name "DevPact" \
        --osx-bundle-identifier "app.devpact.main" \
        $ICON_ARG \
        --add-data "state.py:." \
        --add-data "agents.py:." \
        --add-data "discussion.py:." \
        --add-data "code_reader.py:." \
        --hidden-import "langgraph" \
        --hidden-import "langgraph.graph" \
        --hidden-import "langgraph.pregel" \
        --hidden-import "langgraph.channels" \
        --hidden-import "langgraph.func" \
        --hidden-import "langchain" \
        --hidden-import "langchain_core" \
        --hidden-import "langchain_core.messages" \
        --hidden-import "langchain_core.prompts" \
        --hidden-import "langchain_core.output_parsers" \
        --hidden-import "langchain_openai" \
        --hidden-import "langchain_openai.chat_models" \
        --hidden-import "pydantic" \
        --hidden-import "pydantic.v1" \
        --hidden-import "openai" \
        --hidden-import "httpx" \
        --hidden-import "httpcore" \
        --hidden-import "anyio" \
        --hidden-import "anyio._backends._asyncio" \
        --hidden-import "sniffio" \
        --hidden-import "h11" \
        --hidden-import "certifi" \
        --hidden-import "idna" \
        --hidden-import "charset_normalizer" \
        --hidden-import "dotenv" \
        --hidden-import "jsonpatch" \
        --hidden-import "jsonpointer" \
        --hidden-import "tenacity" \
        --hidden-import "distro" \
        --hidden-import "jiter" \
        --hidden-import "tqdm" \
        --hidden-import "langsmith" \
        --hidden-import "yaml" \
        --hidden-import "annotated_types" \
        --hidden-import "PIL" \
        --hidden-import "PIL.Image" \
        --hidden-import "numpy" \
        --hidden-import "tiktoken" \
        --hidden-import "regex" \
        --hidden-import "packaging" \
        --hidden-import "typing_extensions" \
        --collect-all "langgraph" \
        --collect-all "langchain" \
        --collect-all "langchain_openai" \
        --collect-all "langchain_core" \
        --collect-all "pydantic" \
        --collect-all "openai" \
        --noupx \
        app.py
    
    if [ -f "Info.plist" ]; then
        cp Info.plist "dist/DevPact.app/Contents/Info.plist"
        echo "Info.plist copied to app bundle"
    fi
    
    echo ""
    echo "Signing the application..."
    codesign --force --deep --sign - "dist/DevPact.app" 2>/dev/null || echo "Note: Codesign skipped (may need admin privileges)"
    
    echo ""
    echo "Creating DMG installer..."
    
    DMG_NAME="DevPact-Installer.dmg"
    DMG_VOLUME="DevPact"
    
    # 清理旧文件
    rm -f "dist/$DMG_NAME" 2>/dev/null
    
    # 创建临时目录用于 DMG 内容
    TMP_DIR=$(mktemp -d)
    echo "Using temp directory: $TMP_DIR"
    
    # 复制应用到临时目录
    cp -R "dist/DevPact.app" "$TMP_DIR/"
    
    # 创建 Applications 文件夹快捷方式
    ln -s /Applications "$TMP_DIR/Applications"
    
    # 创建 DMG
    hdiutil create -volname "$DMG_VOLUME" -srcfolder "$TMP_DIR" -ov -format UDZO "dist/$DMG_NAME"
    
    # 清理临时目录
    rm -rf "$TMP_DIR"
    
    if [ -f "dist/$DMG_NAME" ]; then
        echo ""
        echo "✅ DMG created successfully: dist/$DMG_NAME"
        echo "✅ DMG size: $(du -h "dist/$DMG_NAME" | cut -f1)"
        echo ""
        echo "📝 安装说明:"
        echo "   1. 双击打开 DMG 文件"
        echo "   2. 将 DevPact.app 拖拽到 Applications 文件夹"
        echo "   3. 从 Applications 文件夹启动应用"
    else
        echo "❌ DMG creation failed, but app bundle is ready"
    fi
    
    echo ""
    echo "🎉 Build complete!"
    echo "   - App: dist/DevPact.app"
    echo "   - DMG: dist/$DMG_NAME"
    echo ""
    echo "⚠️  If you see 'app is damaged' error, run:"
    echo "   xattr -cr /Applications/DevPact.app"
    
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Building for Linux..."
    
    pyinstaller --noconfirm --onefile \
        --name "devpact" \
        --add-data "state.py:." \
        --add-data "agents.py:." \
        --add-data "discussion.py:." \
        --add-data "code_reader.py:." \
        --hidden-import "langgraph" \
        --hidden-import "langgraph.graph" \
        --hidden-import "langgraph.pregel" \
        --hidden-import "langgraph.channels" \
        --hidden-import "langgraph.func" \
        --hidden-import "langchain" \
        --hidden-import "langchain_core" \
        --hidden-import "langchain_core.messages" \
        --hidden-import "langchain_core.prompts" \
        --hidden-import "langchain_core.output_parsers" \
        --hidden-import "langchain_openai" \
        --hidden-import "langchain_openai.chat_models" \
        --hidden-import "pydantic" \
        --hidden-import "pydantic.v1" \
        --hidden-import "openai" \
        --hidden-import "httpx" \
        --hidden-import "httpcore" \
        --hidden-import "anyio" \
        --hidden-import "anyio._backends._asyncio" \
        --hidden-import "sniffio" \
        --hidden-import "h11" \
        --hidden-import "certifi" \
        --hidden-import "idna" \
        --hidden-import "charset_normalizer" \
        --hidden-import "dotenv" \
        --hidden-import "jsonpatch" \
        --hidden-import "jsonpointer" \
        --hidden-import "tenacity" \
        --hidden-import "distro" \
        --hidden-import "jiter" \
        --hidden-import "tqdm" \
        --hidden-import "langsmith" \
        --hidden-import "yaml" \
        --hidden-import "annotated_types" \
        --collect-all "langgraph" \
        --collect-all "langchain" \
        --collect-all "langchain_openai" \
        --collect-all "langchain_core" \
        --collect-all "pydantic" \
        --collect-all "openai" \
        --noupx \
        app.py
    
    echo ""
    echo "Build complete! Executable located at: dist/devpact"
fi

echo ""
echo "=========================================="
echo "Build finished!"
echo "=========================================="
