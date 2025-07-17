"""
 ================================================
 WaterReminder source code
 Copyright (c) 2025 Lemonsuqing. All rights reserved.

 This code is part of the WaterReminder project.
 Unauthorized copying or distribution is prohibited.
 ================================================
"""
import sys
import os
import winreg
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTimeEdit, QTextEdit, QPushButton, QMessageBox,
    QSystemTrayIcon, QMenu, QApplication, QComboBox, QHBoxLayout,
    QSpinBox, QLabel, QStackedWidget, QListWidget, QListWidgetItem,
    QAbstractItemView
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTime, Qt, QDate
from reminder import Reminder


class WaterReminderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("喝水小助手")
        self.resize(600, 400)

        # 使用堆叠布局来切换主界面和任务列表界面
        self.stacked_widget = QStackedWidget()

        # 创建主界面
        self.main_widget = QWidget()
        self.setup_main_ui()

        # 创建任务列表界面
        self.task_list_widget = QWidget()
        self.setup_task_list_ui()

        # 添加到堆叠布局
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.addWidget(self.task_list_widget)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_widget)
        self.setLayout(main_layout)

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

        # 加载保存的配置
        self.reminder.load_config()
        self.update_task_list()
        self.show()

    def setup_main_ui(self):
        layout = QVBoxLayout()

        # 顶部按钮栏
        top_btn_layout = QHBoxLayout()
        self.task_list_btn = QPushButton("查看提醒任务")
        self.task_list_btn.clicked.connect(self.show_task_list)
        top_btn_layout.addWidget(self.task_list_btn)
        layout.addLayout(top_btn_layout)

        # 提醒周期选择
        period_layout = QHBoxLayout()
        period_layout.addWidget(QLabel("提醒周期:"))
        self.period_combo = QComboBox()
        self.period_combo.addItems(["每小时", "每日", "每周", "每月", "每年"])
        self.period_combo.currentTextChanged.connect(self.update_time_inputs)
        period_layout.addWidget(self.period_combo)
        layout.addLayout(period_layout)

        # 时间输入控件区域
        self.time_input_layout = QHBoxLayout()
        self.create_time_inputs()
        layout.addLayout(self.time_input_layout)

        # 提醒内容
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("输入提醒内容")
        layout.addWidget(self.text_edit)

        # 开机启动选项
        startup_layout = QHBoxLayout()
        startup_layout.addWidget(QLabel("开机启动:"))
        self.startup_combo = QComboBox()
        self.startup_combo.addItems(["否", "是"])
        self.startup_combo.currentTextChanged.connect(self.update_startup_setting)
        startup_layout.addWidget(self.startup_combo)
        layout.addLayout(startup_layout)

        # 开始按钮
        self.start_btn = QPushButton("添加提醒")
        self.start_btn.clicked.connect(self.add_reminder)
        layout.addWidget(self.start_btn)

        self.main_widget.setLayout(layout)

    def setup_task_list_ui(self):
        layout = QVBoxLayout()

        # 顶部按钮栏
        top_btn_layout = QHBoxLayout()
        self.back_btn = QPushButton("返回主界面")
        self.back_btn.clicked.connect(self.show_main)
        top_btn_layout.addWidget(self.back_btn)
        layout.addLayout(top_btn_layout)

        # 任务列表
        self.task_list = QListWidget()
        self.task_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        layout.addWidget(self.task_list)

        # 操作按钮
        btn_layout = QHBoxLayout()
        self.edit_btn = QPushButton("编辑任务")
        self.edit_btn.clicked.connect(self.edit_task)
        self.delete_btn = QPushButton("删除任务")
        self.delete_btn.clicked.connect(self.delete_task)
        self.toggle_btn = QPushButton("暂停/启用")
        self.toggle_btn.clicked.connect(self.toggle_task)
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.delete_btn)
        btn_layout.addWidget(self.toggle_btn)
        layout.addLayout(btn_layout)

        self.task_list_widget.setLayout(layout)

    def create_time_inputs(self):
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

    def update_startup_setting(self, value):
        app_name = "WaterReminder"
        exe_path = os.path.abspath(sys.argv[0])
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_ALL_ACCESS) as regkey:
                if value == "是":
                    winreg.SetValueEx(regkey, app_name, 0, winreg.REG_SZ, exe_path)
                elif value == "否":
                    try:
                        winreg.DeleteValue(regkey, app_name)
                    except FileNotFoundError:
                        pass
        except Exception as e:
            QMessageBox.warning(self, "开机启动设置失败", str(e))

        # 保存配置
        self.reminder.save_config()

    def add_reminder(self):
        period = self.period_combo.currentText()
        content = self.text_edit.toPlainText().strip() or "喝水时间到啦！多喝热水 ❤️"

        task = {
            "period": period,
            "content": content,
            "enabled": True
        }

        if period == "每小时":
            task["minute"] = self.minute_spin.value()
        elif period == "每日":
            task["time"] = self.time_edit.time().toString("HH:mm")
        elif period == "每周":
            task["day"] = self.day_combo.currentIndex() + 1
            task["time"] = self.time_edit.time().toString("HH:mm")
        elif period == "每月":
            task["day"] = self.day_spin.value()
            task["time"] = self.time_edit.time().toString("HH:mm")
        elif period == "每年":
            task["month"] = self.month_spin.value()
            task["day"] = self.day_spin.value()
            task["time"] = self.time_edit.time().toString("HH:mm")

        self.reminder.add_task(task)
        self.update_task_list()

        QMessageBox.information(self, "提示", "提醒任务已添加")
        self.text_edit.clear()

    def show_task_list(self):
        self.update_task_list()
        self.stacked_widget.setCurrentIndex(1)

    def show_main(self):
        self.stacked_widget.setCurrentIndex(0)

    def update_task_list(self):
        self.task_list.clear()
        for i, task in enumerate(self.reminder.tasks):
            item = QListWidgetItem()
            status = "✓" if task["enabled"] else "✗"

            if task["period"] == "每小时":
                text = f"[{status}] 每小时 {task['minute']:02d} 分 - {task['content']}"
            elif task["period"] == "每日":
                text = f"[{status}] 每天 {task['time']} - {task['content']}"
            elif task["period"] == "每周":
                days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
                day_name = days[task['day']-1]
                text = f"[{status}] 每周 {day_name} {task['time']} - {task['content']}"
            elif task["period"] == "每月":
                text = f"[{status}] 每月 {task['day']} 日 {task['time']} - {task['content']}"
            elif task["period"] == "每年":
                text = f"[{status}] 每年 {task['month']} 月 {task['day']} 日 {task['time']} - {task['content']}"

            item.setText(text)
            item.setData(Qt.ItemDataRole.UserRole, i)  # 存储任务索引
            self.task_list.addItem(item)

    def get_selected_task_index(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请先选择一个任务")
            return None
        return selected_items[0].data(Qt.ItemDataRole.UserRole)

    def edit_task(self):
        index = self.get_selected_task_index()
        if index is None:
            return

        task = self.reminder.tasks[index]
        self.show_main()
        self.period_combo.setCurrentText(task["period"])

        if task["period"] == "每小时":
            self.minute_spin.setValue(task["minute"])
        elif task["period"] == "每日":
            self.time_edit.setTime(QTime.fromString(task["time"], "HH:mm"))
        elif task["period"] == "每周":
            self.day_combo.setCurrentIndex(task["day"] - 1)
            self.time_edit.setTime(QTime.fromString(task["time"], "HH:mm"))
        elif task["period"] == "每月":
            self.day_spin.setValue(task["day"])
            self.time_edit.setTime(QTime.fromString(task["time"], "HH:mm"))
        elif task["period"] == "每年":
            self.month_spin.setValue(task["month"])
            self.day_spin.setValue(task["day"])
            self.time_edit.setTime(QTime.fromString(task["time"], "HH:mm"))

        self.text_edit.setPlainText(task["content"])
        self.reminder.remove_task(index)
        self.start_btn.setText("更新提醒")

    def delete_task(self):
        index = self.get_selected_task_index()
        if index is None:
            return

        reply = QMessageBox.question(
            self, "确认删除", "确定要删除这个提醒任务吗?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.reminder.remove_task(index)
            self.update_task_list()

    def toggle_task(self):
        index = self.get_selected_task_index()
        if index is None:
            return

        self.reminder.tasks[index]["enabled"] = not self.reminder.tasks[index]["enabled"]
        self.reminder.save_config()
        self.update_task_list()

    def closeEvent(self, event):
        # 保存配置
        self.reminder.save_config()

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
        # 保存配置
        self.reminder.save_config()

        self.tray_icon.hide()
        QApplication.quit()