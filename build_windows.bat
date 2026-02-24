@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ==========================================
echo DevPact - Windows Build Script
echo ==========================================
echo.

echo Cleaning old build files...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del /q *.spec
if exist __pycache__ rmdir /s /q __pycache__
if exist state\__pycache__ rmdir /s /q state\__pycache__
if exist agents\__pycache__ rmdir /s /q agents\__pycache__
if exist discussion\__pycache__ rmdir /s /q discussion\__pycache__
if exist code_reader\__pycache__ rmdir /s /q code_reader\__pycache__
echo Clean complete!
echo.

echo Checking Python version...
python --version
if errorlevel 1 (
    echo Error: Python not found! Please install Python 3.10 or higher.
    exit /b 1
)
echo.

echo Installing dependencies...
python -m pip install --upgrade pip
pip install pyinstaller PyQt6 langgraph langchain langchain-openai pydantic python-dotenv
echo.

echo Building Windows executable...
pyinstaller --noconfirm --onefile --windowed ^
    --name "DevPact" ^
    --add-data "state.py;." ^
    --add-data "agents.py;." ^
    --add-data "discussion.py;." ^
    --add-data "code_reader.py;." ^
    --hidden-import "langgraph" ^
    --hidden-import "langgraph.graph" ^
    --hidden-import "langgraph.pregel" ^
    --hidden-import "langgraph.channels" ^
    --hidden-import "langgraph.func" ^
    --hidden-import "langchain" ^
    --hidden-import "langchain_core" ^
    --hidden-import "langchain_core.messages" ^
    --hidden-import "langchain_core.prompts" ^
    --hidden-import "langchain_core.output_parsers" ^
    --hidden-import "langchain_openai" ^
    --hidden-import "langchain_openai.chat_models" ^
    --hidden-import "pydantic" ^
    --hidden-import "pydantic.v1" ^
    --hidden-import "openai" ^
    --hidden-import "httpx" ^
    --hidden-import "httpcore" ^
    --hidden-import "anyio" ^
    --hidden-import "anyio._backends._asyncio" ^
    --hidden-import "sniffio" ^
    --hidden-import "h11" ^
    --hidden-import "certifi" ^
    --hidden-import "idna" ^
    --hidden-import "charset_normalizer" ^
    --hidden-import "dotenv" ^
    --hidden-import "jsonpatch" ^
    --hidden-import "jsonpointer" ^
    --hidden-import "tenacity" ^
    --hidden-import "distro" ^
    --hidden-import "jiter" ^
    --hidden-import "tqdm" ^
    --hidden-import "langsmith" ^
    --hidden-import "yaml" ^
    --hidden-import "annotated_types" ^
    --hidden-import "PIL" ^
    --hidden-import "PIL.Image" ^
    --hidden-import "numpy" ^
    --hidden-import "tiktoken" ^
    --hidden-import "regex" ^
    --hidden-import "packaging" ^
    --hidden-import "typing_extensions" ^
    --collect-all "langgraph" ^
    --collect-all "langchain" ^
    --collect-all "langchain_openai" ^
    --collect-all "langchain_core" ^
    --collect-all "pydantic" ^
    --collect-all "openai" ^
    --noupx ^
    app.py

if errorlevel 1 (
    echo Build failed!
    exit /b 1
)

echo.
echo ==========================================
echo Build complete!
echo ==========================================
echo.
echo Executable: dist\DevPact.exe
echo.
echo You can now distribute the executable or create an installer.
echo.
