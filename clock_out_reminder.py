import sys
import os
import winreg
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from gui import WaterReminderWindow

if __name__ == "__main__":
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_path, 'assets', '1.ico')
    # icon_path = r"D:\other\other_tool\drink2\assets\clock_out.ico"

    # print("base_path =", base_path)
    # print("icon_path =", icon_path)

    app_name = "ClockOutReminder"
    exe_path = os.path.abspath(sys.argv[0])

    # 注册表开机启动
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except Exception as e:
        print("写注册表失败", e)

    app = QApplication(sys.argv)
    window = WaterReminderWindow()

    # 改标题和托盘提示
    window.setWindowTitle("下班打卡")
    window.tray_icon.setToolTip("下班打卡")
    window.tray_icon.setIcon(QIcon(icon_path))

    window.time_edit.setTime(window.time_edit.time().fromString("18:00", "HH:mm"))
    window.text_edit.setText("下班打卡")
    window.reminder.start(window.time_edit.time(), window.text_edit.toPlainText())

    window.hide()
    sys.exit(app.exec())
