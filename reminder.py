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


class Reminder:
    def __init__(self, parent):
        self.parent = parent
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_time)
        self.reminder_type = None
        self.reminder_params = {}
        self.reminder_content = ""
        self.last_reminded_day = -1  # 用于每日检查

    def start_hourly(self, minute, content):
        self.reminder_type = "hourly"
        self.reminder_params = {"minute": minute}
        self.reminder_content = content
        self.timer.start(1000)  # 每秒检查一次

    def start_daily(self, time, content):
        self.reminder_type = "daily"
        self.reminder_params = {"time": time}
        self.reminder_content = content
        self.timer.start(1000)

    def start_weekly(self, day, time, content):
        self.reminder_type = "weekly"
        self.reminder_params = {"day": day, "time": time}
        self.reminder_content = content
        self.timer.start(1000)

    def start_monthly(self, day, time, content):
        self.reminder_type = "monthly"
        self.reminder_params = {"day": day, "time": time}
        self.reminder_content = content
        self.timer.start(1000)

    def start_yearly(self, month, day, time, content):
        self.reminder_type = "yearly"
        self.reminder_params = {"month": month, "day": day, "time": time}
        self.reminder_content = content
        self.timer.start(1000)

    def stop(self):
        self.timer.stop()

    def check_time(self):
        now = QTime.currentTime()
        today = QDate.currentDate()

        if self.reminder_type == "hourly":
            if now.minute() == self.reminder_params["minute"] and now.second() == 0:
                self.show_reminder()

        elif self.reminder_type == "daily":
            if (now.hour() == self.reminder_params["time"].hour() and
                    now.minute() == self.reminder_params["time"].minute() and
                    now.second() == 0):
                self.show_reminder()

        elif self.reminder_type == "weekly":
            if (today.dayOfWeek() == self.reminder_params["day"] and
                    now.hour() == self.reminder_params["time"].hour() and
                    now.minute() == self.reminder_params["time"].minute() and
                    now.second() == 0):
                self.show_reminder()

        elif self.reminder_type == "monthly":
            if (today.day() == self.reminder_params["day"] and
                    now.hour() == self.reminder_params["time"].hour() and
                    now.minute() == self.reminder_params["time"].minute() and
                    now.second() == 0):
                self.show_reminder()

        elif self.reminder_type == "yearly":
            if (today.month() == self.reminder_params["month"] and
                    today.day() == self.reminder_params["day"] and
                    now.hour() == self.reminder_params["time"].hour() and
                    now.minute() == self.reminder_params["time"].minute() and
                    now.second() == 0):
                self.show_reminder()

    def show_reminder(self):
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("喝水提醒")
        msg.setText(self.reminder_content)
        msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg.exec()