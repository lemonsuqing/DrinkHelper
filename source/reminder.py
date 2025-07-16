"""
 ================================================
 WaterReminder Build Script
 Copyright (c) 2025 Lemonsuqing. All rights reserved.

 This build script is part of the WaterReminder project.
 Unauthorized copying or distribution is prohibited.
 ================================================
"""
from PyQt6.QtCore import QTimer, QTime, Qt, QDate
from PyQt6.QtWidgets import QMessageBox


class ReminderTask:
    def __init__(self):
        self.period = ""  # "hourly", "daily", "weekly", "monthly", "yearly"
        self.minute = 0   # for hourly
        self.time = QTime()  # for daily, weekly, monthly, yearly
        self.day = 1      # for weekly (1-7), monthly (1-31), yearly (1-31)
        self.month = 1    # for yearly (1-12)
        self.content = ""
        self.enabled = True

    def get_description(self):
        if self.period == "每小时":
            return f"每小时 {self.minute:02d} 分 - {self.content}"
        elif self.period == "每日":
            return f"每天 {self.time.toString('HH:mm')} - {self.content}"
        elif self.period == "每周":
            days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
            return f"每周 {days[self.day-1]} {self.time.toString('HH:mm')} - {self.content}"
        elif self.period == "每月":
            return f"每月 {self.day} 日 {self.time.toString('HH:mm')} - {self.content}"
        elif self.period == "每年":
            return f"每年 {self.month} 月 {self.day} 日 {self.time.toString('HH:mm')} - {self.content}"
        return ""


class Reminder:
    def __init__(self, parent):
        self.parent = parent
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_tasks)
        self.timer.start(1000)  # 每秒检查一次
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)

    def check_tasks(self):
        now = QTime.currentTime()
        today = QDate.currentDate()

        for task in self.tasks:
            if not task.enabled:
                continue

            if task.period == "每小时":
                if now.minute() == task.minute and now.second() == 0:
                    self.show_reminder(task.content)

            elif task.period == "每日":
                if (now.hour() == task.time.hour() and
                        now.minute() == task.time.minute() and
                        now.second() == 0):
                    self.show_reminder(task.content)

            elif task.period == "每周":
                if (today.dayOfWeek() == task.day and
                        now.hour() == task.time.hour() and
                        now.minute() == task.time.minute() and
                        now.second() == 0):
                    self.show_reminder(task.content)

            elif task.period == "每月":
                if (today.day() == task.day and
                        now.hour() == task.time.hour() and
                        now.minute() == task.time.minute() and
                        now.second() == 0):
                    self.show_reminder(task.content)

            elif task.period == "每年":
                if (today.month() == task.month and
                        today.day() == task.day and
                        now.hour() == task.time.hour() and
                        now.minute() == task.time.minute() and
                        now.second() == 0):
                    self.show_reminder(task.content)

    def show_reminder(self, content):
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("喝水提醒")
        msg.setText(content)
        msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg.exec()