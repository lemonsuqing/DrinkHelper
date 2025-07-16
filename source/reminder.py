from PyQt6.QtCore import QTimer, QTime, Qt, QDate
from PyQt6.QtWidgets import QMessageBox
import json
import os


class Reminder:
    CONFIG_FILE = "water_reminder_config.json"

    def __init__(self, parent):
        self.parent = parent
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_tasks)
        self.timer.start(1000)  # 每秒检查一次
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        self.save_config()

    def remove_task(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_config()

    def check_tasks(self):
        now = QTime.currentTime()
        today = QDate.currentDate()

        for task in self.tasks:
            if not task["enabled"]:
                continue

            if task["period"] == "每小时":
                if now.minute() == task["minute"] and now.second() == 0:
                    self.show_reminder(task["content"])

            elif task["period"] == "每日":
                task_time = QTime.fromString(task["time"], "HH:mm")
                if (now.hour() == task_time.hour() and
                        now.minute() == task_time.minute() and
                        now.second() == 0):
                    self.show_reminder(task["content"])

            elif task["period"] == "每周":
                task_time = QTime.fromString(task["time"], "HH:mm")
                if (today.dayOfWeek() == task["day"] and
                        now.hour() == task_time.hour() and
                        now.minute() == task_time.minute() and
                        now.second() == 0):
                    self.show_reminder(task["content"])

            elif task["period"] == "每月":
                task_time = QTime.fromString(task["time"], "HH:mm")
                if (today.day() == task["day"] and
                        now.hour() == task_time.hour() and
                        now.minute() == task_time.minute() and
                        now.second() == 0):
                    self.show_reminder(task["content"])

            elif task["period"] == "每年":
                task_time = QTime.fromString(task["time"], "HH:mm")
                if (today.month() == task["month"] and
                        today.day() == task["day"] and
                        now.hour() == task_time.hour() and
                        now.minute() == task_time.minute() and
                        now.second() == 0):
                    self.show_reminder(task["content"])

    def show_reminder(self, content):
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("喝水提醒")
        msg.setText(content)
        msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg.exec()

    def save_config(self):
        config = {
            "tasks": self.tasks,
            "startup_enabled": self.parent.startup_combo.currentText() == "是"
        }
        try:
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def load_config(self):
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)

                    # 加载任务
                    self.tasks = config.get("tasks", [])

                    # 加载开机启动设置
                    if config.get("startup_enabled", False):
                        self.parent.startup_combo.setCurrentText("是")
                        # 确保注册表中有启动项
                        self.update_startup_setting(True)
                    else:
                        self.parent.startup_combo.setCurrentText("否")
        except Exception as e:
            print(f"加载配置失败: {e}")

    def update_startup_setting(self, enabled):
        app_name = "WaterReminder"
        exe_path = os.path.abspath(sys.argv[0])
        key = r"Software\Microsoft\Windows\CurrentVersion\Run"
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_ALL_ACCESS) as regkey:
                if enabled:
                    winreg.SetValueEx(regkey, app_name, 0, winreg.REG_SZ, exe_path)
                else:
                    try:
                        winreg.DeleteValue(regkey, app_name)
                    except FileNotFoundError:
                        pass
        except Exception as e:
            print(f"更新开机启动设置失败: {e}")