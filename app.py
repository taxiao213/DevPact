# -*- coding: utf-8 -*-
import sys
import os
import threading
import queue
from datetime import datetime
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFileDialog,
    QGroupBox, QSplitter, QProgressBar, QMessageBox, QTabWidget,
    QPlainTextEdit, QStatusBar, QSpinBox, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QCheckBox, QFrame, QScrollArea,
    QSizePolicy, QGraphicsDropShadowEffect, QSpacerItem, QSizePolicy as QSP,
    QGraphicsOpacityEffect, QSplashScreen
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings, QSize, QPropertyAnimation, QEasingCurve, QPoint, QTimer, QPropertyAnimation
from PyQt6.QtGui import QFont, QTextCursor, QColor, QAction, QPalette, QLinearGradient, QPainter, QIcon, QPixmap, QPen

from dotenv import load_dotenv

load_dotenv()

from state import DevelopmentState, ProjectConfig
from code_reader import CodeReader


COLORS = {
    'primary': '#3B82F6',
    'primary_hover': '#2563EB',
    'primary_active': '#1D4ED8',
    'primary_light': '#EFF6FF',
    'secondary': '#F8FAFC',
    'secondary_hover': '#F1F5F9',
    'text_primary': '#0F172A',
    'text_secondary': '#475569',
    'text_light': '#94A3B8',
    'border': '#E2E8F0',
    'border_light': '#F1F5F9',
    'background': '#FFFFFF',
    'success': '#10B981',
    'success_light': '#ECFDF5',
    'error': '#EF4444',
    'error_light': '#FEF2F2',
    'warning': '#F59E0B',
    'warning_light': '#FFFBEB',
    'supervisor': '#3B82F6',
    'frontend': '#10B981',
    'backend': '#F59E0B',
    'discussion': '#8B5CF6',
    'system': '#64748B',
}


MODELS = {
    "Zhipu GLM": [
        "glm-5",
        "glm-4.7",
        "glm-4.6",
        "glm-4.5",
        "glm-4.5v-flash",
        "glm-4.5-air"
    ],
    "Qwen": [
        "qwen3.5-plus-2026-02-15",
        "qwen3.5-397b",
        "qwen3.5-plus",
        "qwen3-coder-plus",
        "qwen3",
        "qwen-image-2.0",
        "qwen2.5-max",
        "qwen2.5-plus",
        "qwen2.5-turbo",
        "qwen-vl-max",
        "qwen-coder-plus",
        "qwen-mt",
        "qwen-max",
        "qwen-plus",
        "qwen-turbo",
    ],
    "Doubao": [
        "doubao-seed-2.0",
        "doubao-2.0-pro",
        "doubao-2.0-lite",
        "doubao-2.0-mini",
        "doubao-2.0-code",
        "doubao-1.5-pro",
        "doubao-1.5-pro-256k",
        "doubao-pro-32k",
        "doubao-lite-32k",
    ],
    "Kimi": [
        "kimi-k2.5",
        "kimi-k2"
    ],
    "MiniMax": [
        "minimax-m2.5",
        "minimax-m2.1",
        "minimax-m2"
    ],
    "DeepSeek": [
        "deepseek-v3.2",
        "deepseek-v3.2-exp",
        "deepseek-v3.2-speciale",
        "deepseek-r1",
        "deepseek-chat",
        "deepseek-coder",
        "deepseek-reasoner",
    ],
    "Claude": [
        "claude-opus-4.6",
        "claude-opus-4.5",
        "claude-sonnet-4.6",
        "claude-sonnet-4-20250514",
        "claude-3-5-sonnet-20241022"
    ],
    "OpenAI": [
        "gpt-5.3",
        "gpt-5.2",
        "gpt-5.2-instant",
        "gpt-5.2-thinking",
        "gpt-5.2-pro",
        "gpt-5.2-codex",
        "gpt-5.1-codex",
        "gpt-5.1-codex-max",
        "gpt-4.5",
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-4",
        "o3-mini",
        "o1",
        "o1-pro",
    ],
    "Gemini": [
        "gemini-3.1-pro",
        "gemini-3-deep-think",
        "gemini-3-pro",
        "gemini-2.5-pro",
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-pro",
        "gemini-1.5-flash",
    ]
}

LANGUAGES = {
    "zh": {
        "app_title": "多Agent协同开发",
        "file": "文件",
        "help": "帮助",
        "about": "关于",
        "exit": "退出",
        "settings": "设置",
        "language": "语言",
        "model": "模型",
        "rounds": "轮次",
        "frontend_path": "前端路径",
        "backend_path": "后端路径",
        "requirement_input": "需求输入",
        "requirement_placeholder": "请详细描述您的开发需求...",
        "start_development": "开始开发",
        "stop": "停止",
        "live_discussion": "实时讨论",
        "contract": "契约文档",
        "frontend": "前端任务",
        "backend": "后端任务",
        "download": "下载",
        "api_configuration": "API 配置",
        "api_key": "API Key",
        "base_url": "Base URL",
        "discussion_config": "讨论配置",
        "max_rounds": "最大轮次",
        "recommended": "推荐: 3-5",
        "cancel": "取消",
        "save": "保存",
        "api_ready": "API 已配置",
        "no_api_key": "未配置 API",
        "warning": "警告",
        "please_enter_requirement": "请输入需求描述",
        "please_configure_api": "请先在设置中配置 API Key",
        "in_progress": "协同开发进行中...",
        "stopped": "已停止",
        "complete": "协同开发完成!",
        "failed": "协同开发失败",
        "no_contract": "暂无契约文档",
        "no_frontend_tasks": "暂无前端任务",
        "no_backend_tasks": "暂无后端任务",
        "success": "成功",
        "saved_to": "已保存到: ",
        "reading_project": "正在读取项目代码...",
        "frontend_files": "前端文件",
        "backend_files": "后端文件",
        "existing_apis": "现有接口",
        "received": "收到需求",
        "max_rounds_model": "最大轮次",
        "starting_distribution": "开始分发任务...",
        "breaking_tasks": "正在拆解任务...",
        "task_complete": "任务拆解完成",
        "tasks": "个任务",
        "endpoints": "个接口",
        "created_proposals": "创建了接口提案",
        "participating": "参与讨论中...",
        "round": "轮次",
        "all_agreed": "所有接口已达成一致!",
        "max_rounds_reached": "达到最大轮次",
        "no_endpoints_warning": "未生成接口提案，请检查需求描述是否清晰",
        "contract_generated": "契约文档已生成!",
        "about_text": "DevPact v1.0.0\n\n基于 LangGraph 的多Agent协同开发工具，\n支持前后端Agent协同讨论，\n自动生成开发契约文档。\n\nGitHub: https://github.com/taxiao213/DevPact\n\n关注我的微信公众号: 他晓",
        "optional": "可选",
        "custom_model_hint": "可直接输入自定义模型名称",
        "enter_api_key": "输入 API Key",
        "base_url_example": "例如: https://open.bigmodel.cn/api/paas/v4",
        "select_frontend_path": "选择前端路径",
        "select_backend_path": "选择后端路径",
        "save_title": "保存",
        "markdown_files": "Markdown 文件 (*.md);;所有文件 (*)",
        "task_breakdown": "任务拆解",
        "generated": "生成时间",
        "task_list": "任务列表",
        "related_apis": "相关接口",
        "description": "描述",
        "author": "他晓",
        "version": "v1.0.0",
        "lang_changed": "语言已切换",
        "verifying_api": "正在验证 API Key...",
        "api_valid": "API Key 验证成功!",
        "api_invalid": "API Key 验证失败，请检查",
        "api_error": "API 验证出错: ",
    },
    "en": {
        "app_title": "DevPact",
        "file": "File",
        "help": "Help",
        "about": "About",
        "exit": "Exit",
        "settings": "Settings",
        "language": "Language",
        "model": "Model",
        "rounds": "Rounds",
        "frontend_path": "Frontend Path",
        "backend_path": "Backend Path",
        "requirement_input": "Requirement Input",
        "requirement_placeholder": "Describe your development requirements...",
        "start_development": "Start Development",
        "stop": "Stop",
        "live_discussion": "Live Discussion",
        "contract": "Contract",
        "frontend": "Frontend",
        "backend": "Backend",
        "download": "Download",
        "api_configuration": "API Configuration",
        "api_key": "API Key",
        "base_url": "Base URL",
        "discussion_config": "Discussion Configuration",
        "max_rounds": "Max Rounds",
        "recommended": "Recommended: 3-5",
        "cancel": "Cancel",
        "save": "Save",
        "api_ready": "API Ready",
        "no_api_key": "No API Key",
        "warning": "Warning",
        "please_enter_requirement": "Please enter requirement description",
        "please_configure_api": "Please configure API Key in Settings first",
        "in_progress": "Collaborative development in progress...",
        "stopped": "Stopped",
        "complete": "Collaborative development complete!",
        "failed": "Collaborative development failed",
        "no_contract": "No contract document",
        "no_frontend_tasks": "No frontend tasks",
        "no_backend_tasks": "No backend tasks",
        "success": "Success",
        "saved_to": "Saved to: ",
        "reading_project": "Reading project code...",
        "frontend_files": "Frontend files",
        "backend_files": "Backend files",
        "existing_apis": "Existing APIs",
        "received": "Received",
        "max_rounds_model": "Max rounds",
        "starting_distribution": "Starting task distribution...",
        "breaking_tasks": "Breaking down tasks...",
        "task_complete": "Task breakdown complete",
        "tasks": "tasks",
        "endpoints": "endpoints",
        "created_proposals": "Created API proposals",
        "participating": "Participating in discussion...",
        "round": "Round",
        "all_agreed": "All APIs agreed!",
        "max_rounds_reached": "Max rounds reached",
        "no_endpoints_warning": "No API proposals generated, please check if requirement description is clear",
        "contract_generated": "Contract document generated!",
        "about_text": "DevPact v1.0.0\n\nA multi-agent collaborative development tool based on LangGraph,\nsupporting frontend and backend agent collaborative discussion,\nautomatically generating development contract documents.\n\nGitHub: https://github.com/taxiao213/DevPact\n\nFollow our WeChat Official Account: 他晓",
        "optional": "Optional",
        "custom_model_hint": "You can enter a custom model name directly",
        "enter_api_key": "Enter your API Key",
        "base_url_example": "e.g., https://open.bigmodel.cn/api/paas/v4",
        "select_frontend_path": "Select Frontend Path",
        "select_backend_path": "Select Backend Path",
        "save_title": "Save",
        "markdown_files": "Markdown Files (*.md);;All Files (*)",
        "task_breakdown": "Task Breakdown",
        "generated": "Generated",
        "task_list": "Task List",
        "related_apis": "Related APIs",
        "description": "Description",
        "author": "Taxiao",
        "version": "v1.0.0",
        "lang_changed": "Language changed",
        "verifying_api": "Verifying API Key...",
        "api_valid": "API Key verified successfully!",
        "api_invalid": "API Key verification failed",
        "api_error": "API verification error: ",
    }
}


def create_robot_icon():
    pixmap = QPixmap(128, 128)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    painter.setBrush(QColor(COLORS['primary']))
    painter.setPen(Qt.PenStyle.NoPen)
    
    painter.drawRoundedRect(24, 40, 80, 72, 16, 16)
    
    painter.drawRoundedRect(16, 20, 20, 24, 8, 8)
    painter.drawRoundedRect(92, 20, 20, 24, 8, 8)
    
    painter.setBrush(QColor('#FFFFFF'))
    painter.drawEllipse(40, 60, 20, 20)
    painter.drawEllipse(68, 60, 20, 20)
    
    painter.setBrush(QColor(COLORS['primary_light']))
    painter.drawRoundedRect(44, 92, 40, 8, 4, 4)
    
    painter.end()
    return QIcon(pixmap)


class LoadingSpinner(QWidget):
    def __init__(self, parent=None, size=24, color=None):
        super().__init__(parent)
        self.size = size
        self.color = color or QColor(COLORS['primary'])
        self.angle = 0
        self.setFixedSize(size, size)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.rotate)
        
    def start(self):
        self.timer.start(50)
        self.show()
        
    def stop(self):
        self.timer.stop()
        self.hide()
        
    def rotate(self):
        self.angle = (self.angle + 15) % 360
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        painter.translate(self.size / 2, self.size / 2)
        painter.rotate(self.angle)
        
        pen = QPen(self.color, 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        
        rect_size = self.size - 6
        painter.drawArc(int(-rect_size/2), int(-rect_size/2), rect_size, rect_size, 0, 270 * 16)


class LoadingDialog(QDialog):
    def __init__(self, parent=None, message="Loading..."):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setFixedSize(180, 120)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.spinner = LoadingSpinner(self, size=48, color=QColor(COLORS['primary']))
        layout.addWidget(self.spinner, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.label = QLabel(message)
        self.label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_primary']};
                font-size: 14px;
                font-weight: 500;
            }}
        """)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(COLORS['background']))
        painter.setPen(QPen(QColor(COLORS['border']), 1))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 16, 16)
        
    def start(self):
        self.spinner.start()
        self.show()
        
    def stop(self):
        self.spinner.stop()
        self.hide()
        self.close()


class CustomMessageBox(QDialog):
    def __init__(self, parent=None, title="Message", message="", icon_type="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)
        self.setMinimumWidth(380)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)
        
        title_row = QHBoxLayout()
        icon_label = QLabel()
        icon_label.setPixmap(create_robot_icon().pixmap(32, 32))
        title_row.addWidget(icon_label)
        
        title_label = QLabel(title)
        title_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_primary']};
                font-size: 16px;
                font-weight: 600;
            }}
        """)
        title_row.addWidget(title_label)
        title_row.addStretch()
        layout.addLayout(title_row)
        
        self.message_label = QLabel(message)
        self.message_label.setStyleSheet(f"""
            QLabel {{
                color: {COLORS['text_secondary']};
                font-size: 14px;
                line-height: 1.5;
            }}
        """)
        self.message_label.setWordWrap(True)
        self.message_label.setMinimumWidth(300)
        layout.addWidget(self.message_label)
        
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        
        ok_btn = QPushButton("OK")
        ok_btn.setFixedSize(80, 32)
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
        """)
        ok_btn.clicked.connect(self.accept)
        btn_row.addWidget(ok_btn)
        layout.addLayout(btn_row)
        
        self.adjustSize()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(COLORS['background']))
        painter.setPen(QPen(QColor(COLORS['border']), 1))
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), 16, 16)


class ToastWidget(QFrame):
    def __init__(self, parent=None, message="", duration=2000):
        super().__init__(parent)
        self.duration = duration
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 16, 24, 16)
        layout.setSpacing(12)
        
        icon_label = QLabel()
        icon_label.setPixmap(create_robot_icon().pixmap(24, 24))
        layout.addWidget(icon_label)
        
        label = QLabel(message)
        label.setStyleSheet(f"""
            QLabel {{
                color: white;
                font-size: 15px;
                font-weight: 500;
            }}
        """)
        layout.addWidget(label)
        
        self.setStyleSheet(f"""
            QFrame {{
                background-color: rgba(30, 30, 30, 0.92);
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
        """)
        
        self.adjustSize()
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0.0)
        
        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        
        self.hide_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.hide_animation.setDuration(200)
        self.hide_animation.setStartValue(1.0)
        self.hide_animation.setEndValue(0.0)
        self.hide_animation.finished.connect(self.hide)
    
    def show_toast(self):
        self.animation.start()
        self.show()
        
        QTimer.singleShot(self.duration, self.start_hide)
    
    def start_hide(self):
        self.hide_animation.start()


class SettingsDialog(QDialog):
    def __init__(self, parent=None, lang="zh"):
        super().__init__(parent)
        self.parent_window = parent
        self.lang = lang
        self.t = LANGUAGES[lang]
        self.setWindowTitle(self.t["settings"])
        self.setMinimumWidth(520)
        self.settings = QSettings(
            QSettings.Format.IniFormat,
            QSettings.Scope.UserScope,
            "MultiAgentDev",
            "MultiAgentDev"
        )
        self.init_ui()
        self.load_settings()
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {COLORS['background']};
            }}
        """)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel(f"⚙️ {self.t['settings']}")
        title.setStyleSheet(f"font-size: 18px; font-weight: 600; color: {COLORS['text_primary']}; margin-bottom: 8px;")
        layout.addWidget(title)

        api_group = QGroupBox(f"🔑 {self.t['api_configuration']}")
        api_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 14px;
                font-weight: 500;
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                margin-top: 12px;
                padding: 16px 12px 12px 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }}
        """)
        api_layout = QVBoxLayout(api_group)
        api_layout.setSpacing(12)

        key_layout = QHBoxLayout()
        key_label = QLabel(self.t["api_key"])
        key_label.setFixedWidth(80)
        key_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText(self.t["enter_api_key"])
        self.api_key_edit.setFixedHeight(36)
        self.api_key_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 0 12px;
                color: {COLORS['text_primary']};
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS['primary']};
            }}
        """)
        self.show_key_btn = QPushButton("👁")
        self.show_key_btn.setCheckable(True)
        self.show_key_btn.setFixedSize(36, 36)
        self.show_key_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary_hover']};
            }}
        """)
        self.show_key_btn.clicked.connect(self.toggle_key_visibility)
        key_layout.addWidget(key_label)
        key_layout.addWidget(self.api_key_edit)
        key_layout.addWidget(self.show_key_btn)
        api_layout.addLayout(key_layout)

        url_layout = QHBoxLayout()
        url_label = QLabel(self.t["base_url"])
        url_label.setFixedWidth(80)
        url_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.base_url_edit = QLineEdit()
        self.base_url_edit.setPlaceholderText(self.t["base_url_example"])
        self.base_url_edit.setFixedHeight(36)
        self.base_url_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 0 12px;
                color: {COLORS['text_primary']};
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS['primary']};
            }}
        """)
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.base_url_edit)
        api_layout.addLayout(url_layout)

        model_layout = QHBoxLayout()
        model_label = QLabel(self.t["model"])
        model_label.setFixedWidth(80)
        model_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.model_combo = QComboBox()
        self.model_combo.setEditable(True)
        self.model_combo.setInsertPolicy(QComboBox.InsertPolicy.InsertAtBottom)
        self.model_combo.setFixedHeight(36)
        self.model_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 0 12px;
                color: {COLORS['text_primary']};
            }}
            QComboBox:focus {{
                border: 1px solid {COLORS['primary']};
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid {COLORS['border']};
                background-color: {COLORS['background']};
                outline: none;
            }}
            QComboBox QAbstractItemView::item {{
                padding: 6px 12px;
                color: {COLORS['text_primary']};
                background-color: transparent;
            }}
            QComboBox QAbstractItemView::item:selected {{
                background-color: {COLORS['primary_light']};
                color: {COLORS['primary']};
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: {COLORS['secondary_hover']};
            }}
            QComboBox QAbstractItemView::item:disabled {{
                color: {COLORS['text_light']};
                background-color: transparent;
            }}
        """)
        
        for provider, models in MODELS.items():
            separator = f"─── {provider} ───"
            self.model_combo.addItem(separator)
            last_index = self.model_combo.count() - 1
            self.model_combo.model().item(last_index).setEnabled(False)
            for model in models:
                self.model_combo.addItem(model)
        
        model_layout.addWidget(model_label)
        model_layout.addWidget(self.model_combo)
        api_layout.addLayout(model_layout)

        hint_label = QLabel(f"💡 {self.t['custom_model_hint']}")
        hint_label.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 12px; margin-left: 80px;")
        api_layout.addWidget(hint_label)

        layout.addWidget(api_group)

        discussion_group = QGroupBox(f"💬 {self.t['discussion_config']}")
        discussion_group.setStyleSheet(f"""
            QGroupBox {{
                font-size: 14px;
                font-weight: 500;
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                margin-top: 12px;
                padding: 16px 12px 12px 12px;
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 4px;
            }}
        """)
        discussion_layout = QVBoxLayout(discussion_group)
        discussion_layout.setSpacing(12)

        rounds_layout = QHBoxLayout()
        rounds_label = QLabel(self.t["max_rounds"])
        rounds_label.setFixedWidth(80)
        rounds_label.setStyleSheet(f"color: {COLORS['text_secondary']};")
        self.max_rounds_spin = QSpinBox()
        self.max_rounds_spin.setRange(1, 20)
        self.max_rounds_spin.setValue(3)
        self.max_rounds_spin.setFixedHeight(36)
        self.max_rounds_spin.setMinimumWidth(80)
        rounds_layout.addWidget(rounds_label)
        rounds_layout.addWidget(self.max_rounds_spin)
        rounds_layout.addStretch()
        
        rounds_hint = QLabel(self.t["recommended"])
        rounds_hint.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 12px;")
        rounds_layout.addWidget(rounds_hint)
        
        discussion_layout.addLayout(rounds_layout)

        layout.addWidget(discussion_group)
        layout.addStretch()

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.addStretch()
        
        cancel_btn = QPushButton(self.t["cancel"])
        cancel_btn.setFixedWidth(90)
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 8px 16px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary_hover']};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        self.save_btn = QPushButton(f"✓ {self.t['save']}")
        self.save_btn.setFixedWidth(90)
        self.save_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
        """)
        self.save_btn.clicked.connect(self.verify_and_save)
        btn_layout.addWidget(self.save_btn)
        
        layout.addLayout(btn_layout)

    def toggle_key_visibility(self):
        if self.show_key_btn.isChecked():
            self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.show_key_btn.setText("🔒")
        else:
            self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.show_key_btn.setText("👁")

    def load_settings(self):
        self.api_key_edit.setText(self.settings.value("api_key", ""))
        self.base_url_edit.setText(self.settings.value("base_url", "https://open.bigmodel.cn/api/paas/v4"))
        model = self.settings.value("model", "glm-4.7")
        index = self.model_combo.findText(model)
        if index >= 0:
            self.model_combo.setCurrentIndex(index)
        else:
            self.model_combo.setEditText(model)
        self.max_rounds_spin.setValue(int(self.settings.value("max_rounds", 3)))
        
        self._original_api_key = self.api_key_edit.text()
        self._original_base_url = self.base_url_edit.text()
        self._original_model = self.model_combo.currentText()

    def save_settings(self):
        self.settings.setValue("api_key", self.api_key_edit.text())
        self.settings.setValue("base_url", self.base_url_edit.text())
        self.settings.setValue("model", self.model_combo.currentText())
        self.settings.setValue("max_rounds", self.max_rounds_spin.value())
        os.environ["OPENAI_API_KEY"] = self.api_key_edit.text()
        os.environ["OPENAI_BASE_URL"] = self.base_url_edit.text()

    def verify_and_save(self):
        api_key = self.api_key_edit.text().strip()
        base_url = self.base_url_edit.text().strip()
        model = self.model_combo.currentText()
        
        api_key_changed = api_key != self._original_api_key
        base_url_changed = base_url != self._original_base_url
        model_changed = model != self._original_model
        
        if not api_key and not api_key_changed:
            self.save_settings()
            self.accept()
            return
        
        if not api_key_changed and not base_url_changed and not model_changed:
            self.save_settings()
            self.accept()
            return
        
        if not api_key:
            self.save_settings()
            self.accept()
            return
        
        self.save_btn.setEnabled(False)
        
        loading_dialog = LoadingDialog(self, self.t["verifying_api"])
        loading_dialog.move(
            self.geometry().center().x() - loading_dialog.width() // 2,
            self.geometry().center().y() - loading_dialog.height() // 2
        )
        loading_dialog.start()
        QApplication.processEvents()
        
        try:
            from langchain_openai import ChatOpenAI
            
            llm = ChatOpenAI(
                model=self.model_combo.currentText(),
                api_key=api_key,
                base_url=self.base_url_edit.text(),
                timeout=10,
            )
            
            response = llm.invoke("Hi", max_tokens=5)
            
            loading_dialog.stop()
            self.save_settings()
            
            if self.parent_window:
                self.parent_window.show_toast(self.t["api_valid"])
            
            self.accept()
            
        except Exception as e:
            loading_dialog.stop()
            error_msg = str(e)[:50]
            CustomMessageBox(self, self.t["warning"], f"{self.t['api_error']}{error_msg}").exec()
            self.save_btn.setEnabled(True)


class AgentWorker(QThread):
    log_signal = pyqtSignal(str, str)
    finished_signal = pyqtSignal(object)
    progress_signal = pyqtSignal(int)

    def __init__(self, requirement: str, frontend_path: str, backend_path: str, 
                 max_rounds: int = 3, model: str = "glm-4.7", lang: str = "zh"):
        super().__init__()
        self.requirement = requirement
        self.frontend_path = frontend_path
        self.backend_path = backend_path
        self.max_rounds = max_rounds
        self.model = model
        self.state = None
        self.lang = lang
        self.t = LANGUAGES[lang]

    def log(self, agent: str, message: str):
        self.log_signal.emit(agent, message)

    def run(self):
        try:
            project_config = ProjectConfig(
                frontend_path=self.frontend_path,
                backend_path=self.backend_path,
            )

            self.state = DevelopmentState(
                requirement=self.requirement,
                project_config=project_config,
                max_rounds=self.max_rounds,
            )

            from agents import SupervisorAgent, FrontendAgent, BackendAgent
            from discussion import DiscussionManager
            
            code_reader = CodeReader()
            supervisor = SupervisorAgent(model=self.model, lang=self.lang)
            frontend = FrontendAgent(model=self.model, lang=self.lang)
            backend = BackendAgent(model=self.model, lang=self.lang)
            discussion_manager = DiscussionManager(lang=self.lang)

            self.progress_signal.emit(5)

            if self.frontend_path or self.backend_path:
                self.log("System", f"📂 {self.t['reading_project']}")
                self.state = code_reader.read_project(self.state)
                self.log("System", f"{self.t['frontend_files']}: {len(self.state.code_context.frontend_files)}")
                self.log("System", f"{self.t['backend_files']}: {len(self.state.code_context.backend_files)}")
                self.log("System", f"{self.t['existing_apis']}: {len(self.state.code_context.existing_apis)}")

            self.progress_signal.emit(10)

            self.log("Supervisor", f"📋 {self.t['received']}: {self.requirement[:80]}...")
            if self.frontend_path:
                self.log("Supervisor", f"📁 Frontend: {self.frontend_path}")
            if self.backend_path:
                self.log("Supervisor", f"📁 Backend: {self.backend_path}")
            self.log("Supervisor", f"🔄 {self.t['max_rounds_model']}: {self.max_rounds}, Model: {self.model}")
            self.log("Supervisor", f"🚀 {self.t['starting_distribution']}")

            self.progress_signal.emit(20)

            self.log("Frontend", f"📝 {self.t['breaking_tasks']}")
            self.state = frontend.breakdown_tasks(self.state)
            if self.state.frontend_breakdown:
                self.log("Frontend", f"✅ {self.t['task_complete']}: {len(self.state.frontend_breakdown.tasks)} {self.t['tasks']}, {len(self.state.frontend_breakdown.endpoints)} {self.t['endpoints']}")
                for i, task in enumerate(self.state.frontend_breakdown.tasks[:3], 1):
                    self.log("Frontend", f"  {i}. {task[:50]}...")
            else:
                self.log("Frontend", f"⚠️ {self.t['log_analysis_failed']}")

            self.progress_signal.emit(40)

            self.log("Backend", f"📝 {self.t['breaking_tasks']}")
            self.state = backend.breakdown_tasks(self.state)
            if self.state.backend_breakdown:
                self.log("Backend", f"✅ {self.t['task_complete']}: {len(self.state.backend_breakdown.tasks)} {self.t['tasks']}, {len(self.state.backend_breakdown.endpoints)} {self.t['endpoints']}")
                for i, task in enumerate(self.state.backend_breakdown.tasks[:3], 1):
                    self.log("Backend", f"  {i}. {task[:50]}...")
            else:
                self.log("Backend", f"⚠️ {self.t['log_analysis_failed']}")

            self.progress_signal.emit(50)

            self.state = discussion_manager.create_proposals(self.state)
            self.log("Discussion", f"📤 {self.t['created_proposals']}: {len(self.state.schema_proposals)}")

            self.progress_signal.emit(60)

            while True:
                self.log("Frontend", f"💬 {self.t['participating']}")
                self.state, frontend_response = frontend.discuss(self.state)
                self.log("Frontend", frontend_response)

                self.log("Backend", f"💬 {self.t['participating']}")
                self.state, backend_response = backend.discuss(self.state)
                self.log("Backend", backend_response)

                self.state = discussion_manager.process_agreements(self.state)
                self.state.current_round += 1

                self.log("Discussion", f"🔄 {self.t['round']} {self.state.current_round}/{self.state.max_rounds}")

                if len(self.state.agreed_schemas) == len(self.state.schema_proposals) and len(self.state.schema_proposals) > 0:
                    self.log("Discussion", f"✅ {self.t['all_agreed']}")
                    break
                if self.state.current_round >= self.state.max_rounds:
                    self.log("Discussion", f"⏱ {self.t['max_rounds_reached']}")
                    if len(self.state.schema_proposals) == 0:
                        self.log("Discussion", f"⚠️ {self.t['no_endpoints_warning']}")
                    break

                progress = 60 + (self.state.current_round / self.state.max_rounds) * 30
                self.progress_signal.emit(int(progress))

            self.progress_signal.emit(90)

            self.state = supervisor.generate_contract(self.state)
            self.log("Supervisor", f"📄 {self.t['contract_generated']}")

            self.progress_signal.emit(100)

            self.finished_signal.emit(self.state)

        except Exception as e:
            import traceback
            self.log("Error", f"❌ {str(e)}")
            self.log("Error", traceback.format_exc())
            self.finished_signal.emit(None)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings(
            QSettings.Format.IniFormat,
            QSettings.Scope.UserScope,
            "MultiAgentDev",
            "MultiAgentDev"
        )
        self.lang = self.settings.value("language", "zh")
        self.t = LANGUAGES[self.lang]
        self.worker = None
        self.toast = None
        self.current_status = "ready"

        self.setWindowTitle(self.t["app_title"])
        self.setMinimumSize(1100, 700)
        
        self.setWindowIcon(create_robot_icon())
        
        self.init_ui()
        self.load_settings()
        self.apply_env_settings()

    def show_toast(self, message):
        if self.toast:
            self.toast.hide()
        
        self.toast = ToastWidget(self, message, 2000)
        
        geo = self.geometry()
        toast_width = self.toast.width()
        toast_height = self.toast.height()
        
        x = geo.x() + (geo.width() - toast_width) // 2
        y = geo.y() + geo.height() - toast_height - 80
        
        self.toast.move(x, y)
        self.toast.show_toast()

    def update_language(self, new_lang):
        self.lang = new_lang
        self.t = LANGUAGES[new_lang]
        self.settings.setValue("language", new_lang)
        
        self.setWindowTitle(self.t["app_title"])
        
        self.title_label.setText(f"🤖 {self.t['app_title']}")
        self.frontend_path_label.setText(f"🎨 {self.t['frontend_path']}")
        self.backend_path_label.setText(f"⚙️ {self.t['backend_path']}")
        self.requirement_label.setText(f"📝 {self.t['requirement_input']}")
        self.discussion_label.setText(f"💬 {self.t['live_discussion']}")
        self.discussion_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: 600;
                color: {COLORS['text_primary']};
                background-color: transparent;
            }}
        """)
        
        self.frontend_path_edit.setPlaceholderText(self.t["optional"])
        self.backend_path_edit.setPlaceholderText(self.t["optional"])
        self.requirement_edit.setPlaceholderText(self.t["requirement_placeholder"])
        
        self.start_btn.setText(f"🚀 {self.t['start_development']}")
        self.stop_btn.setText(f"⏹ {self.t['stop']}")
        
        self.settings_btn.setText(f"⚙️ {self.t['settings']}")
        
        self.result_tabs.setTabText(0, f"📄 {self.t['contract']}")
        self.result_tabs.setTabText(1, f"🎨 {self.t['frontend']}")
        self.result_tabs.setTabText(2, f"⚙️ {self.t['backend']}")
        
        self.download_contract_btn.setText(f"📥 {self.t['download']}")
        self.download_frontend_btn.setText(f"📥 {self.t['download']}")
        self.download_backend_btn.setText(f"📥 {self.t['download']}")
        
        self.file_menu.setTitle(self.t["file"])
        self.help_menu.setTitle(self.t["help"])
        self.settings_action.setText(self.t["settings"])
        self.exit_action.setText(self.t["exit"])
        self.about_action.setText(self.t["about"])
        
        self.file_menu.clear()
        self.file_menu.addAction(self.settings_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.exit_action)
        
        self.help_menu.clear()
        self.help_menu.addAction(self.about_action)
        
        self.version_label.setText(f"{self.t['author']} | {self.t['version']}")
        
        status_messages = {
            "ready": "",
            "in_progress": self.t["in_progress"],
            "stopped": self.t["stopped"],
            "complete": f"✅ {self.t['complete']}",
            "failed": self.t["failed"],
        }
        if self.current_status in status_messages:
            self.statusBar().showMessage(status_messages[self.current_status])
        
        self.update_api_status_indicator()
        
        self.show_toast(self.t["lang_changed"])

    def init_ui(self):
        self.create_menu_bar()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        header = self.create_header()
        main_layout.addWidget(header)

        content = self.create_content_area()
        main_layout.addWidget(content, 1)

        footer = self.create_footer()
        main_layout.addWidget(footer)

    def create_header(self):
        header = QFrame()
        header.setFixedHeight(50)
        header.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
                border-bottom: 1px solid {COLORS['border']};
            }}
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(16, 0, 16, 0)

        self.title_label = QLabel(f"🤖 {self.t['app_title']}")
        self.title_label.setStyleSheet(f"""
            font-size: 16px;
            font-weight: 600;
            color: {COLORS['text_primary']};
        """)
        layout.addWidget(self.title_label)

        layout.addStretch()

        self.api_status_indicator = QLabel()
        self.update_api_status_indicator()
        layout.addWidget(self.api_status_indicator)

        layout.addSpacing(12)

        self.lang_combo = QComboBox()
        self.lang_combo.addItem("中文", "zh")
        self.lang_combo.addItem("EN", "en")
        current_lang_index = 0 if self.lang == "zh" else 1
        self.lang_combo.setCurrentIndex(current_lang_index)
        self.lang_combo.setFixedWidth(70)
        self.lang_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {COLORS['secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 4px 8px;
                font-size: 12px;
                color: {COLORS['text_primary']};
            }}
            QComboBox:hover {{
                border: 1px solid {COLORS['primary']};
            }}
            QComboBox QAbstractItemView {{
                border: 1px solid {COLORS['border']};
                background-color: {COLORS['background']};
                outline: none;
            }}
            QComboBox QAbstractItemView::item {{
                padding: 4px 8px;
                color: {COLORS['text_primary']};
                background-color: transparent;
            }}
            QComboBox QAbstractItemView::item:selected {{
                background-color: {COLORS['primary_light']};
                color: {COLORS['primary']};
            }}
            QComboBox QAbstractItemView::item:hover {{
                background-color: {COLORS['secondary_hover']};
            }}
        """)
        self.lang_combo.currentIndexChanged.connect(self.on_language_changed)
        layout.addWidget(self.lang_combo)

        layout.addSpacing(8)

        self.settings_btn = QPushButton(f"⚙️ {self.t['settings']}")
        self.settings_btn.setFixedHeight(32)
        self.settings_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 0 16px;
                font-size: 13px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary_hover']};
                border: 1px solid {COLORS['primary']};
            }}
        """)
        self.settings_btn.clicked.connect(self.show_settings_dialog)
        layout.addWidget(self.settings_btn)

        return header

    def create_footer(self):
        footer = QFrame()
        footer.setFixedHeight(28)
        footer.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['secondary']};
                border-top: 1px solid {COLORS['border']};
            }}
        """)
        
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(16, 0, 16, 0)

        layout.addStretch()

        self.version_label = QLabel(f"{self.t['author']} | {self.t['version']}")
        self.version_label.setStyleSheet(f"color: {COLORS['text_light']}; font-size: 11px;")
        layout.addWidget(self.version_label)

        layout.addStretch()

        return footer

    def create_content_area(self):
        content = QWidget()
        content.setStyleSheet(f"background-color: {COLORS['background']};")
        layout = QVBoxLayout(content)
        layout.setSpacing(16)
        layout.setContentsMargins(20, 20, 20, 20)

        config_group = QFrame()
        config_group.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)
        config_layout = QHBoxLayout(config_group)
        config_layout.setSpacing(16)
        config_layout.setContentsMargins(16, 12, 16, 12)

        frontend_section = QVBoxLayout()
        self.frontend_path_label = QLabel(f"🎨 {self.t['frontend_path']}")
        self.frontend_path_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 500;")
        frontend_section.addWidget(self.frontend_path_label)
        
        frontend_row = QHBoxLayout()
        self.frontend_path_edit = QLineEdit()
        self.frontend_path_edit.setPlaceholderText(self.t["optional"])
        self.frontend_path_edit.setMinimumWidth(250)
        self.frontend_path_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 6px 10px;
                color: {COLORS['text_primary']};
                font-size: 12px;
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS['primary']};
            }}
        """)
        self.frontend_browse_btn = QPushButton("📁")
        self.frontend_browse_btn.setFixedSize(30, 26)
        self.frontend_browse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary_hover']};
            }}
        """)
        self.frontend_browse_btn.clicked.connect(self.browse_frontend_path)
        frontend_row.addWidget(self.frontend_path_edit)
        frontend_row.addWidget(self.frontend_browse_btn)
        frontend_section.addLayout(frontend_row)
        config_layout.addLayout(frontend_section)

        backend_section = QVBoxLayout()
        self.backend_path_label = QLabel(f"⚙️ {self.t['backend_path']}")
        self.backend_path_label.setStyleSheet(f"color: {COLORS['text_secondary']}; font-size: 12px; font-weight: 500;")
        backend_section.addWidget(self.backend_path_label)
        
        backend_row = QHBoxLayout()
        self.backend_path_edit = QLineEdit()
        self.backend_path_edit.setPlaceholderText(self.t["optional"])
        self.backend_path_edit.setMinimumWidth(250)
        self.backend_path_edit.setStyleSheet(f"""
            QLineEdit {{
                background-color: {COLORS['secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 6px 10px;
                color: {COLORS['text_primary']};
                font-size: 12px;
            }}
            QLineEdit:focus {{
                border: 1px solid {COLORS['primary']};
            }}
        """)
        self.backend_browse_btn = QPushButton("📁")
        self.backend_browse_btn.setFixedSize(30, 26)
        self.backend_browse_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary_hover']};
            }}
        """)
        self.backend_browse_btn.clicked.connect(self.browse_backend_path)
        backend_row.addWidget(self.backend_path_edit)
        backend_row.addWidget(self.backend_browse_btn)
        backend_section.addLayout(backend_row)
        config_layout.addLayout(backend_section)

        config_layout.addStretch()
        layout.addWidget(config_group)

        input_group = QFrame()
        input_group.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)
        input_layout = QVBoxLayout(input_group)
        input_layout.setSpacing(12)
        input_layout.setContentsMargins(16, 16, 16, 16)

        title_row = QHBoxLayout()
        self.requirement_label = QLabel(f"📝 {self.t['requirement_input']}")
        self.requirement_label.setStyleSheet(f"font-size: 15px; font-weight: 600; color: {COLORS['text_primary']};")
        title_row.addWidget(self.requirement_label)
        title_row.addStretch()
        input_layout.addLayout(title_row)
        
        self.requirement_edit = QPlainTextEdit()
        self.requirement_edit.setPlaceholderText(self.t["requirement_placeholder"])
        self.requirement_edit.setMinimumHeight(80)
        self.requirement_edit.setMaximumHeight(100)
        self.requirement_edit.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {COLORS['secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 10px;
                color: {COLORS['text_primary']};
                font-size: 13px;
            }}
            QPlainTextEdit:focus {{
                border: 1px solid {COLORS['primary']};
            }}
        """)
        input_layout.addWidget(self.requirement_edit)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(12)
        
        self.start_btn = QPushButton(f"🚀 {self.t['start_development']}")
        self.start_btn.setFixedHeight(36)
        self.start_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {COLORS['primary_hover']};
            }}
            QPushButton:disabled {{
                background-color: {COLORS['text_light']};
            }}
        """)
        self.start_btn.clicked.connect(self.start_collaboration)
        btn_row.addWidget(self.start_btn)

        self.stop_btn = QPushButton(f"⏹ {self.t['stop']}")
        self.stop_btn.setFixedHeight(36)
        self.stop_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['error']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0 20px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: #DC2626;
            }}
            QPushButton:disabled {{
                background-color: {COLORS['text_light']};
            }}
        """)
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_collaboration)
        btn_row.addWidget(self.stop_btn)
        
        btn_row.addStretch()
        input_layout.addLayout(btn_row)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(4)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setStyleSheet(f"""
            QProgressBar {{
                background-color: {COLORS['secondary']};
                border: none;
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background-color: {COLORS['primary']};
                border-radius: 2px;
            }}
        """)
        input_layout.addWidget(self.progress_bar)

        layout.addWidget(input_group)

        result_splitter = QSplitter(Qt.Orientation.Horizontal)
        result_splitter.setStyleSheet(f"""
            QSplitter::handle {{
                background-color: {COLORS['border']};
                width: 1px;
            }}
        """)

        discussion_group = QFrame()
        discussion_group.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)
        discussion_layout = QVBoxLayout(discussion_group)
        discussion_layout.setSpacing(8)
        discussion_layout.setContentsMargins(12, 12, 12, 12)

        self.discussion_label = QLabel(f"💬 {self.t['live_discussion']}")
        self.discussion_label.setStyleSheet(f"""
            QLabel {{
                font-size: 14px;
                font-weight: 600;
                color: {COLORS['text_primary']};
                background-color: transparent;
            }}
        """)
        discussion_layout.addWidget(self.discussion_label)

        self.discussion_text = QTextEdit()
        self.discussion_text.setReadOnly(True)
        self.discussion_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['secondary']};
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
                line-height: 1.6;
            }}
        """)
        discussion_layout.addWidget(self.discussion_text)
        result_splitter.addWidget(discussion_group)

        result_group = QFrame()
        result_group.setStyleSheet(f"""
            QFrame {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
            }}
        """)
        result_layout = QVBoxLayout(result_group)
        result_layout.setSpacing(8)
        result_layout.setContentsMargins(12, 12, 12, 12)

        self.result_tabs = QTabWidget()
        self.result_tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                border: none;
                background-color: {COLORS['background']};
            }}
            QTabBar::tab {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_secondary']};
                border: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                padding: 8px 16px;
                margin-right: 2px;
                font-size: 13px;
            }}
            QTabBar::tab:selected {{
                background-color: {COLORS['background']};
                color: {COLORS['primary']};
                font-weight: 500;
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {COLORS['secondary_hover']};
            }}
        """)

        contract_tab = QWidget()
        contract_layout = QVBoxLayout(contract_tab)
        contract_layout.setContentsMargins(0, 8, 0, 0)
        contract_layout.setSpacing(8)
        self.contract_text = QTextEdit()
        self.contract_text.setReadOnly(True)
        self.contract_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['secondary']};
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
            }}
        """)
        contract_layout.addWidget(self.contract_text)
        
        self.download_contract_btn = QPushButton(f"📥 {self.t['download']}")
        self.download_contract_btn.setFixedHeight(28)
        self.download_contract_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary_hover']};
            }}
        """)
        self.download_contract_btn.clicked.connect(self.download_contract)
        contract_layout.addWidget(self.download_contract_btn)
        self.result_tabs.addTab(contract_tab, f"📄 {self.t['contract']}")

        frontend_tab = QWidget()
        frontend_layout = QVBoxLayout(frontend_tab)
        frontend_layout.setContentsMargins(0, 8, 0, 0)
        frontend_layout.setSpacing(8)
        self.frontend_text = QTextEdit()
        self.frontend_text.setReadOnly(True)
        self.frontend_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['secondary']};
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
            }}
        """)
        frontend_layout.addWidget(self.frontend_text)
        
        self.download_frontend_btn = QPushButton(f"📥 {self.t['download']}")
        self.download_frontend_btn.setFixedHeight(28)
        self.download_frontend_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary_hover']};
            }}
        """)
        self.download_frontend_btn.clicked.connect(self.download_frontend_tasks)
        frontend_layout.addWidget(self.download_frontend_btn)
        self.result_tabs.addTab(frontend_tab, f"🎨 {self.t['frontend']}")

        backend_tab = QWidget()
        backend_layout = QVBoxLayout(backend_tab)
        backend_layout.setContentsMargins(0, 8, 0, 0)
        backend_layout.setSpacing(8)
        self.backend_text = QTextEdit()
        self.backend_text.setReadOnly(True)
        self.backend_text.setStyleSheet(f"""
            QTextEdit {{
                background-color: {COLORS['secondary']};
                border: none;
                border-radius: 6px;
                padding: 10px;
                font-size: 13px;
            }}
        """)
        backend_layout.addWidget(self.backend_text)
        
        self.download_backend_btn = QPushButton(f"📥 {self.t['download']}")
        self.download_backend_btn.setFixedHeight(28)
        self.download_backend_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {COLORS['secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                font-size: 12px;
            }}
            QPushButton:hover {{
                background-color: {COLORS['secondary_hover']};
            }}
        """)
        self.download_backend_btn.clicked.connect(self.download_backend_tasks)
        backend_layout.addWidget(self.download_backend_btn)
        self.result_tabs.addTab(backend_tab, f"⚙️ {self.t['backend']}")

        result_layout.addWidget(self.result_tabs)
        result_splitter.addWidget(result_group)

        result_splitter.setSizes([400, 400])
        layout.addWidget(result_splitter, 1)

        return content

    def create_menu_bar(self):
        self.menubar = self.menuBar()
        self.menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: {COLORS['background']};
                border-bottom: 1px solid {COLORS['border']};
                padding: 2px 8px;
            }}
            QMenuBar::item {{
                padding: 4px 8px;
                border-radius: 4px;
                color: {COLORS['text_primary']};
                font-size: 13px;
            }}
            QMenuBar::item:selected {{
                background-color: {COLORS['secondary']};
            }}
            QMenu {{
                background-color: {COLORS['background']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 4px;
            }}
            QMenu::item {{
                padding: 6px 20px;
                border-radius: 4px;
                font-size: 13px;
            }}
            QMenu::item:selected {{
                background-color: {COLORS['primary_light']};
                color: {COLORS['primary']};
            }}
        """)

        self.file_menu = self.menubar.addMenu(self.t["file"])

        self.settings_action = QAction(self.t["settings"], self)
        self.settings_action.setShortcut("Ctrl+,")
        self.settings_action.triggered.connect(self.show_settings_dialog)
        self.file_menu.addAction(self.settings_action)

        self.file_menu.addSeparator()

        self.exit_action = QAction(self.t["exit"], self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        self.help_menu = self.menubar.addMenu(self.t["help"])

        self.about_action = QAction(self.t["about"], self)
        self.about_action.triggered.connect(self.show_about)
        self.help_menu.addAction(self.about_action)

    def on_language_changed(self, index):
        new_lang = self.lang_combo.currentData()
        if new_lang != self.lang:
            self.update_language(new_lang)

    def load_settings(self):
        self.frontend_path_edit.setText(self.settings.value("frontend_path", ""))
        self.backend_path_edit.setText(self.settings.value("backend_path", ""))

    def apply_env_settings(self):
        api_key = self.settings.value("api_key", "")
        base_url = self.settings.value("base_url", "")
        
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
        if base_url:
            os.environ["OPENAI_BASE_URL"] = base_url
        
        self.update_api_status_indicator()

    def save_settings(self):
        self.settings.setValue("frontend_path", self.frontend_path_edit.text())
        self.settings.setValue("backend_path", self.backend_path_edit.text())

    def update_api_status_indicator(self):
        api_key = self.settings.value("api_key", "")
        if api_key:
            self.api_status_indicator.setText(f"🟢 {self.t['api_ready']}")
            self.api_status_indicator.setStyleSheet(f"color: {COLORS['success']}; font-size: 12px;")
        else:
            self.api_status_indicator.setText(f"🔴 {self.t['no_api_key']}")
            self.api_status_indicator.setStyleSheet(f"color: {COLORS['error']}; font-size: 12px;")

    def show_settings_dialog(self):
        dialog = SettingsDialog(self, self.lang)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.apply_env_settings()
            self.load_settings()

    def show_about(self):
        CustomMessageBox(self, "About", self.t["about_text"]).exec()

    def browse_frontend_path(self):
        path = QFileDialog.getExistingDirectory(self, self.t["select_frontend_path"])
        if path:
            self.frontend_path_edit.setText(path)
            self.save_settings()

    def browse_backend_path(self):
        path = QFileDialog.getExistingDirectory(self, self.t["select_backend_path"])
        if path:
            self.backend_path_edit.setText(path)
            self.save_settings()

    def start_collaboration(self):
        requirement = self.requirement_edit.toPlainText().strip()
        if not requirement:
            CustomMessageBox(self, self.t["warning"], self.t["please_enter_requirement"]).exec()
            return

        api_key = self.settings.value("api_key", "")
        if not api_key:
            CustomMessageBox(self, self.t["warning"], self.t["please_configure_api"]).exec()
            self.show_settings_dialog()
            return

        self.discussion_text.clear()
        self.contract_text.clear()
        self.frontend_text.clear()
        self.backend_text.clear()
        self.progress_bar.setValue(0)

        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)

        model = self.settings.value("model", "glm-4.7")
        max_rounds = int(self.settings.value("max_rounds", 3))

        self.worker = AgentWorker(
            requirement=requirement,
            frontend_path=self.frontend_path_edit.text(),
            backend_path=self.backend_path_edit.text(),
            max_rounds=max_rounds,
            model=model,
            lang=self.lang,
        )
        self.worker.log_signal.connect(self.append_log)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.progress_signal.connect(self.progress_bar.setValue)
        self.worker.start()

        self.current_status = "in_progress"
        self.statusBar().showMessage(self.t["in_progress"])

    def stop_collaboration(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.append_log("System", f"⏹ {self.t['stopped']}")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.current_status = "stopped"
        self.statusBar().showMessage(self.t["stopped"])

    def append_log(self, agent: str, message: str):
        colors = {
            "Supervisor": COLORS['supervisor'],
            "Frontend": COLORS['frontend'],
            "Backend": COLORS['backend'],
            "Discussion": COLORS['discussion'],
            "System": COLORS['system'],
            "Error": COLORS['error'],
        }
        bg_colors = {
            "Supervisor": COLORS['primary_light'],
            "Frontend": COLORS['success_light'],
            "Backend": COLORS['warning_light'],
            "Discussion": '#F3E8FF',
            "System": COLORS['secondary'],
            "Error": COLORS['error_light'],
        }
        color = colors.get(agent, COLORS['text_primary'])
        bg_color = bg_colors.get(agent, COLORS['secondary'])
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        html = f'''
        <div style="margin-bottom: 6px; padding: 8px 10px; background-color: {bg_color}; border-radius: 6px; border-left: 2px solid {color};">
            <span style="color: {COLORS['text_light']}; font-size: 11px;">[{timestamp}]</span>
            <span style="color: {color}; font-weight: 600; font-size: 12px; margin-left: 6px;">{agent}</span>
            <span style="color: {COLORS['text_primary']}; font-size: 13px; margin-left: 4px;">{message}</span>
        </div>
        '''
        self.discussion_text.append(html)
        cursor = self.discussion_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.discussion_text.setTextCursor(cursor)

    def on_finished(self, state: DevelopmentState):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)

        if state is None:
            self.current_status = "failed"
            self.statusBar().showMessage(self.t["failed"])
            return

        self.state = state
        self.contract_text.setPlainText(state.final_contract)

        if state.frontend_breakdown:
            frontend_md = self._generate_task_md(state.frontend_breakdown, self.t["frontend"])
            self.frontend_text.setPlainText(frontend_md)

        if state.backend_breakdown:
            backend_md = self._generate_task_md(state.backend_breakdown, self.t["backend"])
            self.backend_text.setPlainText(backend_md)

        self.current_status = "complete"
        self.statusBar().showMessage(f"✅ {self.t['complete']}")

    def _generate_task_md(self, breakdown, agent_type: str) -> str:
        lines = [f"# {agent_type} {self.t['task_breakdown']}\n"]
        lines.append(f"{self.t['generated']}: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        lines.append(f"## {self.t['task_list']}\n")
        for i, task in enumerate(breakdown.tasks, 1):
            lines.append(f"{i}. {task}\n")

        if breakdown.endpoints:
            lines.append(f"\n## {self.t['related_apis']}\n")
            for ep in breakdown.endpoints:
                lines.append(f"\n### {ep.method} {ep.path}\n")
                lines.append(f"{self.t['description']}: {ep.description}\n")

        return "".join(lines)

    def download_contract(self):
        if not hasattr(self, 'state') or not self.state.final_contract:
            CustomMessageBox(self, self.t["warning"], self.t["no_contract"]).exec()
            return
        self._download_md(self.state.final_contract, self.t["contract"], "contract")

    def download_frontend_tasks(self):
        if not hasattr(self, 'state') or not self.state.frontend_breakdown:
            CustomMessageBox(self, self.t["warning"], self.t["no_frontend_tasks"]).exec()
            return
        content = self._generate_task_md(self.state.frontend_breakdown, self.t["frontend"])
        self._download_md(content, f"{self.t['frontend']} {self.t['task_breakdown']}", "frontend_tasks")

    def download_backend_tasks(self):
        if not hasattr(self, 'state') or not self.state.backend_breakdown:
            CustomMessageBox(self, self.t["warning"], self.t["no_backend_tasks"]).exec()
            return
        content = self._generate_task_md(self.state.backend_breakdown, self.t["backend"])
        self._download_md(content, f"{self.t['backend']} {self.t['task_breakdown']}", "backend_tasks")

    def _download_md(self, content: str, title: str, default_name: str):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"{default_name}_{timestamp}.md"

        path, _ = QFileDialog.getSaveFileName(
            self,
            f"{self.t['save_title']} {title}",
            default_filename,
            self.t["markdown_files"]
        )

        if path:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.show_toast(f"{self.t['saved_to']}{path}")


def main():
    import os
    os.environ["QT_MAC_WANTS_LAYER"] = "1"
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    app.setApplicationName("DevPact")
    app.setApplicationDisplayName("DevPact")
    app.setOrganizationName("DevPact")
    app.setOrganizationDomain("devpact.app")

    font = QFont()
    font.setFamily("PingFang SC")
    font.setPointSize(13)
    app.setFont(font)

    splash_pix = QPixmap(400, 200)
    splash_pix.fill(Qt.GlobalColor.white)
    painter = QPainter(splash_pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    gradient = QLinearGradient(0, 0, 400, 200)
    gradient.setColorAt(0, QColor("#3B82F6"))
    gradient.setColorAt(1, QColor("#2563EB"))
    painter.setBrush(gradient)
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawRoundedRect(0, 0, 400, 200, 20, 20)
    
    painter.setPen(QColor("white"))
    painter.setFont(QFont("Arial", 28, QFont.Weight.Bold))
    painter.drawText(splash_pix.rect(), Qt.AlignmentFlag.AlignCenter, "DevPact")
    
    painter.setFont(QFont("Arial", 12))
    painter.drawText(0, 150, 400, 30, Qt.AlignmentFlag.AlignHCenter, "Loading...")
    painter.end()
    
    splash = QSplashScreen(splash_pix)
    splash.show()
    app.processEvents()

    try:
        app.setWindowIcon(create_robot_icon())
    except:
        pass
    
    if sys.platform == "darwin":
        try:
            from AppKit import NSApplication, NSImage
            ns_app = NSApplication.sharedApplication()
            ns_app.setApplicationName_("DevPact")
        except:
            pass

    try:
        window = MainWindow()
        splash.finish(window)
        window.show()
    except Exception as e:
        splash.close()
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
