@echo off
chcp 65001 >nul
echo ==========================================
echo DevPact - Build Script for Windows
echo ==========================================

set PYTHON_CMD=
where python >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    where python3 >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=python3
    ) else (
        echo Error: Python not found!
        pause
        exit /b 1
    )
)

echo Using Python: %PYTHON_CMD%
%PYTHON_CMD% --version

echo.
echo Installing dependencies...
%PYTHON_CMD% -m pip install pyinstaller PyQt6 langgraph langchain langchain-openai pydantic python-dotenv

echo.
echo Building executable for Windows...

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
    --collect-all "langgraph" ^
    --collect-all "langchain" ^
    --collect-all "langchain_openai" ^
    --collect-all "langchain_core" ^
    --collect-all "pydantic" ^
    --collect-all "openai" ^
    --noupx ^
    app.py

echo.
echo ==========================================
echo Build complete!
echo Executable located at: dist\DevPact.exe
echo ==========================================
pause
