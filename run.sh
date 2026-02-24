#!/bin/bash
# 1. 安装依赖
pip3.13 install -e .

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 OpenAI API Key

# 3. 运行
python3 main.py

# 清除 QSettings 缓存
# rm -rf ~/Library/Preferences/MultiAgentDev.MultiAgentDev.plist
# rm -rf ~/Library/Preferences/com.MultiAgentDev.MultiAgentDev.plist