from PyQt6.QtCore import QTimer, QTime, Qt
from PyQt6.QtWidgets import QMessageBox

class Reminder:
    def __init__(self, parent):
        self.parent = parent
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_time)
        self.reminder_time = None
        self.reminder_content = ""
        self.has_reminded_today = False  # 防止多次提醒

    def start(self, time_qtime, content):
        self.reminder_time = time_qtime
        self.reminder_content = content
        self.has_reminded_today = False
        self.timer.start(1000)  # 每秒检查一次

    def stop(self):
        self.timer.stop()

    def check_time(self):
        now = QTime.currentTime()
        if (now.hour() == self.reminder_time.hour() and
            now.minute() == self.reminder_time.minute()):
            if not self.has_reminded_today:
                self.has_reminded_today = True
                self.show_reminder()
        else:
            self.has_reminded_today = False  # 过了时间点后重置状态

    def show_reminder(self):
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("喝水提醒")
        msg.setText(self.reminder_content or "喝水时间到啦！多喝热水 ❤️")
        msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg.exec()
