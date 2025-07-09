import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTimeEdit, QTextEdit, QPushButton, QMessageBox,
    QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTime, Qt
from reminder import Reminder

class WaterReminderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("喝水小助手")
        self.resize(300, 200)

        self.layout = QVBoxLayout()

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime.currentTime())

        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("输入提醒内容")

        self.start_btn = QPushButton("开始提醒")
        self.start_btn.clicked.connect(self.start_reminder)

        self.layout.addWidget(self.time_edit)
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.start_btn)

        self.setLayout(self.layout)

        self.reminder = Reminder(self)

        # 兼容打包后资源路径
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, 'assets', 'icon.ico')

        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        tray_menu = QMenu()

        show_action = QAction("显示主界面")
        quit_action = QAction("退出程序")

        show_action.triggered.connect(self.show_window)
        quit_action.triggered.connect(self.quit_app)

        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # 启动隐藏窗口，实现后台运行
        # self.hide()
        self.show()

    def start_reminder(self):
        time = self.time_edit.time()
        content = self.text_edit.toPlainText().strip()
        if not content:
            content = "喝水时间到啦！多喝热水 ❤️"

        self.reminder.start(time, content)
        msg = QMessageBox(self)
        msg.setWindowTitle("提示")
        msg.setText(f"提醒已设置为每天 {time.toString('HH:mm')}")
        msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg.exec()

    def show_window(self):
        self.show()
        self.raise_()
        self.activateWindow()

    def quit_app(self):
        self.tray_icon.hide()
        QApplication.quit()
