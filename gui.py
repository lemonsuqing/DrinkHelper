import sys
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTimeEdit, QTextEdit, QPushButton, QMessageBox,
    QSystemTrayIcon, QMenu, QApplication
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QTime, Qt
from reminder import Reminder

class WaterReminderWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("喝水小助手")
        self.resize(300, 200)

        # 布局
        layout = QVBoxLayout()
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime.currentTime())
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("输入提醒内容")
        self.start_btn = QPushButton("开始提醒")
        self.start_btn.clicked.connect(self.start_reminder)

        layout.addWidget(self.time_edit)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.start_btn)
        self.setLayout(layout)

        self.reminder = Reminder(self)

        # ✅ 不设置 parent
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_path, 'assets', 'icon.ico')
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path))  # ❗关键：不要传 self
        self.tray_icon.setToolTip("喝水小助手")

        # ✅ 托盘菜单
        self.menu = QMenu()
        self.show_action = QAction("显示主界面")
        self.quit_action = QAction("退出程序")

        self.show_action.triggered.connect(self.show_window)
        self.quit_action.triggered.connect(self.quit_app)

        self.menu.addAction(self.show_action)
        self.menu.addAction(self.quit_action)

        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

        # ✅ 不绑定 activated 信号
        # self.tray_icon.activated.connect(...)   ❌完全注释掉

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
