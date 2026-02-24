# DevPact - Multi-Agent Collaborative Development Tool

<div align="center">

![DevPact Logo](https://img.shields.io/badge/DevPact-v1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-orange.svg)

**A multi-agent collaborative development tool based on LangGraph, supporting frontend and backend agent collaborative discussion, automatically generating development contract documents**

English | [简体中文](./README.md)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Screenshots](#-screenshots)
- [Supported Platforms](#-supported-platforms)
- [Supported LLMs](#-supported-llms)
- [Installation](#-installation)
- [Build Guide](#-build-guide)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

- 🤖 **Multi-Agent Collaboration** - Three agents (Supervisor, Frontend, Backend) work together
- 💬 **Real-time Discussion** - Frontend and Backend agents discuss API design in real-time
- 📄 **Contract Documents** - Automatically generate development contract documents
- 📝 **Task Breakdown** - Automatically break down frontend and backend development tasks
- 🌐 **Multi-language Support** - Support for Chinese and English interfaces
- 🔧 **Flexible Configuration** - Support for multiple LLM APIs

---

## 📸 Screenshots

### Main Interface

![DevPact Main](./pic/DevPact_03.png)

### Settings

![DevPact Settings](./pic/DevPact_04.png)

![DevPact Settings](./pic/DevPact_05.png)

### Contract Document

![DevPact Contract Document](./pic/DevPact_06.png)

![DevPact Contract Document](./pic/DevPact_07.png)

---

## 💻 Supported Platforms


| Platform    | Architecture                   | Status       | Notes                                   |
| ----------- | ------------------------------ | ------------ | --------------------------------------- |
| **macOS**   | ARM64 (Apple Silicon M1/M2/M3) | ✅ Supported | Recommended for Apple Silicon Mac users |
| **macOS**   | x86-64 (Intel)                 | ✅ Supported | For Intel Mac users                     |
| **Windows** | x86-64 (64-bit)                | ✅ Supported | Recommended for 64-bit Windows users    |
| **Linux**   | x86-64 (64-bit)                | ✅ Supported | Recommended for 64-bit Linux users      |

> ⚠️ **Note**: Due to PyQt6 limitations, Windows x86 (32-bit), Windows ARM64, Linux x86 (32-bit), and Linux ARM architectures are not currently supported.

---

## 🧠 Supported LLMs

### Chinese LLMs


| Provider      | Models                                                                       |
| ------------- | ---------------------------------------------------------------------------- |
| **Zhipu GLM** | glm-5, glm-4.7, glm-4.6, glm-4.5, glm-4.5v-flash, glm-4.5-air                |
| **Qwen**      | qwen3.5-plus, qwen3.5-397b, qwen3-coder-plus, qwen2.5-max, qwen-max, etc.    |
| **Doubao**    | doubao-2.0-pro, doubao-2.0-lite, doubao-1.5-pro, doubao-pro-32k, etc.        |
| **Kimi**      | kimi-k2.5, kimi-k2                                                           |
| **MiniMax**   | minimax-m2.5, minimax-m2.1, minimax-m2                                       |
| **DeepSeek**  | deepseek-v3.2, deepseek-r1, deepseek-chat, deepseek-coder, deepseek-reasoner |

### International LLMs


| Provider   | Models                                                                 |
| ---------- | ---------------------------------------------------------------------- |
| **OpenAI** | gpt-5.3, gpt-5.2, gpt-4.5, gpt-4o, gpt-4o-mini, o3-mini, o1, o1-pro    |
| **Claude** | claude-opus-4.6, claude-opus-4.5, claude-sonnet-4.6, claude-3-5-sonnet |
| **Gemini** | gemini-3.1-pro, gemini-3-deep-think, gemini-2.5-pro, gemini-2.5-flash  |

> 💡 **Tip**: Custom model names are supported - you can enter any model name directly

---

## 📦 Installation

### System Requirements

- Python 3.10 or higher
- pip package manager

### Installation Steps

```bash
# Clone the repository
git clone https://github.com/taxiao213/DevPact.git
cd DevPact

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# or
.\.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### Dependencies

```
PyQt6>=6.4.0
langgraph>=0.2.0
langchain>=0.3.0
langchain-openai>=0.2.0
pydantic>=2.0.0
python-dotenv>=1.0.0
pyinstaller>=6.0.0
```

---

## 🔨 Build Guide

### Local Build

#### macOS

```bash
# Grant execute permission
chmod +x build.sh

# Run build
./build.sh
```

Build artifacts in `dist/` directory:

- `DevPact.app` - macOS application
- `DevPact-Installer.dmg` - DMG installer

#### Windows

```batch
# Run build script
build_windows.bat
```

Build artifacts in `dist/` directory:

- `DevPact.exe` - Windows executable

#### Linux

```bash
chmod +x build.sh
./build.sh
```

Build artifacts in `dist/` directory:

- `devpact` - Linux executable

### GitHub Actions Auto Build

The project supports automatic multi-platform builds via GitHub Actions:

1. Create and push a version tag:

   ```bash
   git tag DEV_PACT1.0.0
   git push origin DEV_PACT1.0.0
   ```
2. GitHub Actions will automatically build the following versions:


   | Platform | Architecture          | Output File                |
   | -------- | --------------------- | -------------------------- |
   | macOS    | ARM64 (Apple Silicon) | `DevPact-macOS-arm64.dmg`  |
   | macOS    | x86-64 (Intel)        | `DevPact-macOS-x64.dmg`    |
   | Windows  | x86-64                | `DevPact-Windows-x64.zip`  |
   | Linux    | x86-64                | `DevPact-Linux-x64.tar.gz` |
3. After the build completes, download the corresponding version from the [GitHub Releases](https://github.com/taxiao213/DevPact/releases) page

---

## 📖 Usage Guide

### Launch the Application

#### Development Mode

```bash
python app.py
```

#### Production Mode

- **macOS**: Double-click `DevPact.app` or launch from Applications after DMG installation
- **Windows**: Double-click `DevPact.exe`
- **Linux**: Run `./devpact`

### Configure API

1. Click the **⚙️ Settings** button in the top right corner
2. Enter your API Key and Base URL
3. Select a model
4. Click **✓ Save**

### Start Development

1. **Set Project Paths** (optional)

   - Frontend Path: Select the frontend project directory
   - Backend Path: Select the backend project directory
2. **Enter Requirements**

   - Describe your development requirements in detail in the input box
3. **Start Development**

   - Click the **🚀 Start Development** button
   - Watch the real-time discussion process
   - View the generated contract documents and task lists
4. **Download Results**

   - Contract Document
   - Frontend Tasks
   - Backend Tasks

### Uninstall Application

#### macOS

```bash
# Run uninstall script
./uninstall.sh
```

Or manually remove:

```bash
rm -rf /Applications/DevPact.app
rm -rf ~/Library/Preferences/app.devpact.main.plist
rm -rf ~/.config/MultiAgentDev
```

#### Windows

Uninstall via Control Panel or directly delete program files

#### Linux

Delete executable and configuration directory:

```bash
rm -rf /usr/local/bin/devpact
rm -rf ~/.config/MultiAgentDev
```

---

## 📁 Project Structure

```
DevPact/
├── app.py              # Main application entry
├── agents.py           # Agent definitions (Supervisor, Frontend, Backend)
├── state.py            # State management
├── workflow.py         # Workflow definition
├── discussion.py       # Discussion management
├── code_reader.py      # Code reader
├── build.sh            # macOS/Linux build script
├── build_windows.bat   # Windows build script
├── uninstall.sh        # macOS uninstall script
├── clear_cache.sh      # Clear cache script
├── requirements.txt    # Python dependencies
├── build.spec          # PyInstaller configuration
├── pic/                # Application screenshots
├── .github/
│   └── workflows/
│       └── release.yml # GitHub Actions configuration
└── README.md           # Project documentation
```

---

## ❓ FAQ

### 1. macOS shows "App is damaged"

```bash
xattr -cr /Applications/DevPact.app
```

### 2. API verification failed

- Check if API Key is correct
- Check if Base URL is correct
- Confirm network connection is working

### 3. Settings not saved

Run the clear cache script and try again:

```bash
./clear_cache.sh
```

### 4. Windows antivirus false positive

Add the program to your antivirus whitelist, or build from source yourself.

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Create a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

---

## 📞 Contact

- **GitHub**: [https://github.com/taxiao213/DevPact](https://github.com/taxiao213/DevPact)
- **WeChat Official Account**: 他晓

---

<div align="center">

**⭐ If this project helps you, please give it a Star! ⭐**

Made with ❤️ by Taxiao

</div>
