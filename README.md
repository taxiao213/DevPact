# DevPact - 多Agent协同开发工具

<div align="center">

![DevPact Logo](https://img.shields.io/badge/DevPact-v1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Windows%20%7C%20Linux-orange.svg)

**基于 LangGraph 的多Agent协同开发工具，支持前后端Agent协同讨论，自动生成开发契约文档**

[English](./README_EN.md) | 简体中文

</div>

---

## 📋 目录

- [功能特性](#-功能特性)
- [支持平台](#-支持平台)
- [支持的大模型](#-支持的大模型)
- [安装依赖](#-安装依赖)
- [构建指南](#-构建指南)
- [使用指南](#-使用指南)
- [项目结构](#-项目结构)
- [常见问题](#-常见问题)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

## ✨ 功能特性

- 🤖 **多Agent协同** - Supervisor、Frontend、Backend 三个 Agent 协同工作
- 💬 **实时讨论** - 前后端 Agent 实时讨论接口设计
- 📄 **契约文档** - 自动生成开发契约文档
- 📝 **任务拆解** - 自动拆解前后端开发任务
- 🌐 **多语言支持** - 支持中文和英文界面
- 🔧 **灵活配置** - 支持多种大模型 API

---

## 💻 支持平台

| 平台 | 架构 | 状态 |
|------|------|------|
| **macOS** | ARM64 (Apple Silicon M1/M2/M3) | ✅ 支持 |
| **macOS** | x86-64 (Intel) | ✅ 支持 |
| **Windows** | x86-64 (64位) | ✅ 支持 |
| **Windows** | x86 (32位) | ✅ 支持 |
| **Windows** | ARM64 (Windows on ARM) | ✅ 支持 |
| **Linux** | x86-64 (64位) | ✅ 支持 |
| **Linux** | x86 (32位) | ✅ 支持 |
| **Linux** | ARM (ARMv7/ARM64) | ✅ 支持 |

---

## 🧠 支持的大模型

### 国内大模型

| 提供商 | 模型列表 |
|--------|----------|
| **智谱 GLM** | glm-5, glm-4.7, glm-4.6, glm-4.5, glm-4.5v-flash, glm-4.5-air |
| **通义千问** | qwen3.5-plus, qwen3.5-397b, qwen3-coder-plus, qwen2.5-max, qwen-max 等 |
| **豆包** | doubao-2.0-pro, doubao-2.0-lite, doubao-1.5-pro, doubao-pro-32k 等 |
| **Kimi** | kimi-k2.5, kimi-k2 |
| **MiniMax** | minimax-m2.5, minimax-m2.1, minimax-m2 |
| **DeepSeek** | deepseek-v3.2, deepseek-r1, deepseek-chat, deepseek-coder, deepseek-reasoner |

### 国际大模型

| 提供商 | 模型列表 |
|--------|----------|
| **OpenAI** | gpt-5.3, gpt-5.2, gpt-4.5, gpt-4o, gpt-4o-mini, o3-mini, o1, o1-pro |
| **Claude** | claude-opus-4.6, claude-opus-4.5, claude-sonnet-4.6, claude-3-5-sonnet |
| **Gemini** | gemini-3.1-pro, gemini-3-deep-think, gemini-2.5-pro, gemini-2.5-flash |

> 💡 **提示**: 支持自定义模型名称，可直接输入任意模型名称

---

## 📦 安装依赖

### 系统要求

- Python 3.10 或更高版本
- pip 包管理器

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/taxiao213/DevPact.git
cd DevPact

# 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或
.\.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 依赖列表

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

## 🔨 构建指南

### 本地构建

#### macOS

```bash
# 赋予执行权限
chmod +x build.sh

# 执行构建
./build.sh
```

构建产物位于 `dist/` 目录：
- `DevPact.app` - macOS 应用程序
- `DevPact-Installer.dmg` - DMG 安装包

#### Windows

```batch
# 执行构建脚本
build_windows.bat
```

构建产物位于 `dist/` 目录：
- `DevPact.exe` - Windows 可执行文件

#### Linux

```bash
chmod +x build.sh
./build.sh
```

构建产物位于 `dist/` 目录：
- `devpact` - Linux 可执行文件

### GitHub Actions 自动构建

项目支持通过 GitHub Actions 自动构建多平台版本：

1. 创建并推送版本标签：
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. GitHub Actions 将自动构建以下版本：
   - macOS ARM64 (Apple Silicon)
   - macOS x86-64 (Intel)
   - Windows x86-64
   - Windows x86
   - Windows ARM64
   - Linux x86-64
   - Linux x86
   - Linux ARM64

3. 构建完成后，在 GitHub Releases 页面下载对应版本

---

## 📖 使用指南

### 启动应用

#### 开发模式

```bash
python app.py
```

#### 生产模式

- **macOS**: 双击 `DevPact.app` 或 DMG 安装后从应用程序启动
- **Windows**: 双击 `DevPact.exe`
- **Linux**: 执行 `./devpact`

### 配置 API

1. 点击右上角 **⚙️ 设置** 按钮
2. 输入 API Key 和 Base URL
3. 选择模型
4. 点击 **✓ 保存**

### 开始开发

1. **设置项目路径**（可选）
   - 前端路径：选择前端项目目录
   - 后端路径：选择后端项目目录

2. **输入需求**
   - 在需求输入框中详细描述开发需求

3. **开始开发**
   - 点击 **🚀 开始开发** 按钮
   - 观察实时讨论过程
   - 查看生成的契约文档和任务列表

4. **下载结果**
   - 契约文档
   - 前端任务
   - 后端任务

### 卸载应用

#### macOS

```bash
# 运行卸载脚本
./uninstall.sh
```

或手动删除：
```bash
rm -rf /Applications/DevPact.app
rm -rf ~/Library/Preferences/app.devpact.main.plist
rm -rf ~/.config/MultiAgentDev
```

#### Windows

通过控制面板卸载或直接删除程序文件

#### Linux

删除可执行文件和配置目录：
```bash
rm -rf /usr/local/bin/devpact
rm -rf ~/.config/MultiAgentDev
```

---

## 📁 项目结构

```
DevPact/
├── app.py              # 主应用程序入口
├── agents.py           # Agent 定义（Supervisor, Frontend, Backend）
├── state.py            # 状态管理
├── workflow.py         # 工作流定义
├── discussion.py       # 讨论管理
├── code_reader.py      # 代码读取器
├── build.sh            # macOS/Linux 构建脚本
├── build_windows.bat   # Windows 构建脚本
├── uninstall.sh        # macOS 卸载脚本
├── clear_cache.sh      # 清理缓存脚本
├── requirements.txt    # Python 依赖
├── build.spec          # PyInstaller 配置
├── .github/
│   └── workflows/
│       └── release.yml # GitHub Actions 配置
└── README.md           # 项目文档
```

---

## ❓ 常见问题

### 1. macOS 提示"应用已损坏"

```bash
xattr -cr /Applications/DevPact.app
```

### 2. API 验证失败

- 检查 API Key 是否正确
- 检查 Base URL 是否正确
- 确认网络连接正常

### 3. 配置未保存

运行清理脚本后重试：
```bash
./clear_cache.sh
```

### 4. Windows 杀毒软件误报

将程序添加到杀毒软件白名单，或从源码自行构建。

---

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 📞 联系方式

- **GitHub**: [https://github.com/taxiao213/DevPact](https://github.com/taxiao213/DevPact)
- **微信公众号**: 他晓

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！⭐**

Made with ❤️ by 他晓

</div>
