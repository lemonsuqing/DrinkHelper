"""
 ================================================
 WaterReminder Build Script
 Copyright (c) 2025 Lemonsuqing. All rights reserved.

 This build script is part of the WaterReminder project.
 Unauthorized copying or distribution is prohibited.
 ================================================
"""
import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTimeEdit, QTextEdit, QPushButton, QMessageBox,
    QSystemTrayIcon, QMenu, QApplication, QComboBox, QHBoxLayout, QSpinBox, QLabel
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTime, Qt, QDate
from reminder import Reminder


class WaterReminderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("喝水小助手")
        self.resize(400, 250)

        # 布局
        layout = QVBoxLayout()

        # 周期选择
        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel("提醒周期:"))
        self.period_combo = QComboBox()
        self.period_combo.addItems(["每小时", "每日", "每周", "每月", "每年"])
        self.period_combo.currentTextChanged.connect(self.update_time_inputs)
        period_layout.addWidget(self.period_combo)
        layout.addLayout(period_layout)

        # 时间输入区域
        self.time_input_layout = QHBoxLayout()
        self.create_time_inputs()
        layout.addLayout(self.time_input_layout)

        # 提醒内容
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("输入提醒内容")
        layout.addWidget(self.text_edit)

        # 开始按钮
        self.start_btn = QPushButton("开始提醒")
        self.start_btn.clicked.connect(self.start_reminder)
        layout.addWidget(self.start_btn)

        self.setLayout(layout)

        self.reminder = Reminder(self)

        # 系统托盘
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, 'assets', 'icon.ico')
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("喝水小助手")

        # 托盘菜单
        self.menu = QMenu()
        self.show_action = QAction("显示主界面")
        self.quit_action = QAction("退出程序")

        self.show_action.triggered.connect(self.show_window)
        self.quit_action.triggered.connect(self.quit_app)

        self.menu.addAction(self.show_action)
        self.menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

        self.show()

    def create_time_inputs(self):
        # 清除旧的小部件
        for i in reversed(range(self.time_input_layout.count())):
            self.time_input_layout.itemAt(i).widget().setParent(None)

        current_period = self.period_combo.currentText()

        if current_period == "每小时":
            self.minute_spin = QSpinBox()
            self.minute_spin.setRange(0, 59)
            self.minute_spin.setValue(0)
            self.time_input_layout.addWidget(QLabel("分钟:"))
            self.time_input_layout.addWidget(self.minute_spin)

        elif current_period == "每日":
            self.time_edit = QTimeEdit()
            self.time_edit.setDisplayFormat("HH:mm")
            self.time_edit.setTime(QTime.currentTime())
            self.time_input_layout.addWidget(QLabel("时间:"))
            self.time_input_layout.addWidget(self.time_edit)

        elif current_period == "每周":
            self.day_combo = QComboBox()
            self.day_combo.addItems(["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"])
            self.time_edit = QTimeEdit()
            self.time_edit.setDisplayFormat("HH:mm")
            self.time_edit.setTime(QTime.currentTime())
            self.time_input_layout.addWidget(QLabel("星期:"))
            self.time_input_layout.addWidget(self.day_combo)
            self.time_input_layout.addWidget(QLabel("时间:"))
            self.time_input_layout.addWidget(self.time_edit)

        elif current_period == "每月":
            self.day_spin = QSpinBox()
            self.day_spin.setRange(1, 31)
            self.day_spin.setValue(QDate.currentDate().day())
            self.time_edit = QTimeEdit()
            self.time_edit.setDisplayFormat("HH:mm")
            self.time_edit.setTime(QTime.currentTime())
            self.time_input_layout.addWidget(QLabel("日:"))
            self.time_input_layout.addWidget(self.day_spin)
            self.time_input_layout.addWidget(QLabel("时间:"))
            self.time_input_layout.addWidget(self.time_edit)

        elif current_period == "每年":
            self.month_spin = QSpinBox()
            self.month_spin.setRange(1, 12)
            self.month_spin.setValue(QDate.currentDate().month())
            self.day_spin = QSpinBox()
            self.day_spin.setRange(1, 31)
            self.day_spin.setValue(QDate.currentDate().day())
            self.time_edit = QTimeEdit()
            self.time_edit.setDisplayFormat("HH:mm")
            self.time_edit.setTime(QTime.currentTime())
            self.time_input_layout.addWidget(QLabel("月:"))
            self.time_input_layout.addWidget(self.month_spin)
            self.time_input_layout.addWidget(QLabel("日:"))
            self.time_input_layout.addWidget(self.day_spin)
            self.time_input_layout.addWidget(QLabel("时间:"))
            self.time_input_layout.addWidget(self.time_edit)

    def update_time_inputs(self):
        self.create_time_inputs()

    def start_reminder(self):
        period = self.period_combo.currentText()
        content = self.text_edit.toPlainText().strip() or "喝水时间到啦！多喝热水 ❤️"

        if period == "每小时":
            minute = self.minute_spin.value()
            self.reminder.start_hourly(minute, content)
            msg_text = f"提醒已设置为每小时 {minute} 分"

        elif period == "每日":
            time = self.time_edit.time()
            self.reminder.start_daily(time, content)
            msg_text = f"提醒已设置为每天 {time.toString('HH:mm')}"

        elif period == "每周":
            day = self.day_combo.currentIndex() + 1  # 1=周一, 7=周日
            time = self.time_edit.time()
            self.reminder.start_weekly(day, time, content)
            msg_text = f"提醒已设置为每周{['一', '二', '三', '四', '五', '六', '日'][day - 1]} {time.toString('HH:mm')}"

        elif period == "每月":
            day = self.day_spin.value()
            time = self.time_edit.time()
            self.reminder.start_monthly(day, time, content)
            msg_text = f"提醒已设置为每月 {day} 日 {time.toString('HH:mm')}"

        elif period == "每年":
            month = self.month_spin.value()
            day = self.day_spin.value()
            time = self.time_edit.time()
            self.reminder.start_yearly(month, day, time, content)
            msg_text = f"提醒已设置为每年 {month} 月 {day} 日 {time.toString('HH:mm')}"

        msg = QMessageBox(self)
        msg.setWindowTitle("提示")
        msg.setText(msg_text)
        msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg.exec()

    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.tray_icon.showMessage(
            "喝水小助手",
            "程序已最小化到托盘，右键点击图标可操作",
            QSystemTrayIcon.MessageIcon.Information,
            3000
        )

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()