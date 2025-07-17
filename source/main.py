"""
 ================================================
 WaterReminder source code
 Copyright (c) 2025 Lemonsuqing. All rights reserved.

 This code is part of the WaterReminder project.
 Unauthorized copying or distribution is prohibited.
 ================================================
"""
from PyQt6.QtWidgets import QApplication
import sys
from gui import WaterReminderWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WaterReminderWindow()
    sys.exit(app.exec())
