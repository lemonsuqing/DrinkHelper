"""
================================================
 WaterReminder - Reminder Module
 Copyright (c) 2025 Lemonsuqing. All rights reserved.

 This module handles the reminder logic and task management.
 Unauthorized copying or distribution is prohibited.
================================================
"""
import json
import os
from PyQt6.QtCore import QTimer, QTime, Qt, QDate
from PyQt6.QtWidgets import QMessageBox


class Reminder:
    CONFIG_FILE = "water_reminder_config.json"

    def __init__(self, parent):
        self.parent = parent
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_tasks)
        self.timer.start(1000)  # 每秒检查一次
        self.tasks = []

    def add_task(self, task):
        """添加新任务并自动排序"""
        self.tasks.append(task)
        self.sort_tasks()
        self.save_config()

    def remove_task(self, index):
        """移除指定索引的任务"""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_config()

    def sort_tasks(self):
        """对任务列表进行排序"""
        # 定义优先级顺序
        period_order = {"每小时": 0, "每日": 1, "每周": 2, "每月": 3, "每年": 4}

        def get_sort_key(task):
            # 主要按周期类型排序
            key = period_order[task["period"]]

            # 次要按时间排序
            if task["period"] == "每小时":
                time_key = task["minute"]
            else:
                # 将时间字符串转换为分钟数便于比较
                h, m = map(int, task["time"].split(":"))
                time_key = h * 60 + m

            # 如果是每周/每月/每年，再按日期排序
            date_key = 0
            if task["period"] == "每周":
                date_key = task["day"]
            elif task["period"] == "每月":
                date_key = task["day"]
            elif task["period"] == "每年":
                date_key = task["month"] * 100 + task["day"]

            return (key, time_key, date_key)

        # 对任务列表进行排序
        self.tasks.sort(key=get_sort_key)

    def check_tasks(self):
        """检查是否有任务需要触发"""
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
        """显示提醒窗口"""
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("喝水提醒")
        msg.setText(content)
        msg.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)
        msg.exec()

    def save_config(self):
        """保存配置到文件"""
        config = {
            "tasks": self.tasks,
            "startup_enabled": getattr(self.parent, "startup_combo", None) and
                               self.parent.startup_combo.currentText() == "是"
        }
        try:
            with open(self.CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存配置失败: {e}")

    def load_config(self):
        """从文件加载配置"""
        try:
            if os.path.exists(self.CONFIG_FILE):
                with open(self.CONFIG_FILE, "r", encoding="utf-8") as f:
                    config = json.load(f)

                    # 加载任务
                    self.tasks = config.get("tasks", [])
                    self.sort_tasks()  # 加载后排序

                    # 加载开机启动设置
                    if config.get("startup_enabled", False):
                        if hasattr(self.parent, "startup_combo"):
                            self.parent.startup_combo.setCurrentText("是")
        except Exception as e:
            print(f"加载配置失败: {e}")

    def update_task_status(self, index, enabled):
        """更新任务启用状态"""
        if 0 <= index < len(self.tasks):
            self.tasks[index]["enabled"] = enabled
            self.save_config()