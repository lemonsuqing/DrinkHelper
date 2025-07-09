from PyQt6.QtWidgets import QApplication
import sys
from gui import WaterReminderWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WaterReminderWindow()
    sys.exit(app.exec())
