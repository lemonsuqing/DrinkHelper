# 喝水小助手 Water Reminder

一个基于 Python 和 PyQt6 的桌面喝水提醒小程序，帮助你养成定时喝水的好习惯。

---

## 功能

- 设置固定时间的喝水提醒
- 自定义提醒内容
- 提醒弹窗始终显示在最前端
- 程序运行在系统托盘，支持最小化后台运行
- 支持关闭命令行窗口（打包为 exe）

---

## 环境要求

- Python 3.7 及以上

---

## 安装与运行

### 1. 安装依赖（如果你想手动运行）

```bash
pip install PyQt6
````

### 2. 运行程序（开发环境）

```bash
pythonw main.py
```

> 使用 `pythonw` 可以避免弹出命令行窗口。

---

### 3. 一键构建（Windows）

双击 `build.cmd`，构建过程中会自动检测并安装依赖（PyQt6、PyInstaller），然后生成独立可执行文件。

生成的可执行文件位置：

* 默认在当前目录下 `WaterReminder.exe`

---

## 卸载构建文件

执行 `Uninstall.cmd` 可以清理构建产生的中间文件和可执行文件，保持项目整洁。

---

## 使用说明

1. 打开程序，选择提醒周期和设置提醒时间
2. 输入提醒内容（可为空，默认“喝水时间到啦！多喝热水 ❤️”）
3. 点击“开始提醒”按钮
4. 程序最小化到系统托盘，定时提醒弹窗会弹出
5. 右键托盘图标可以选择“显示主界面”或“退出程序”

---

## 项目目录结构

```
├── assets/               # 图标资源文件夹
│   └── icon.ico          # 程序托盘图标
├── build.cmd             # 一键安装
├── Uninstall.cmd         # 一键清理
├── WaterReminder.exe     # 构建后生成的可执行文件
├── source/               # 源码
│   ├── gui.py            # 主窗口界面代码
│   ├── main.py           # 程序入口
│   └── reminder.py       # 提醒逻辑代码
├── tool/                 # 依赖wheel包，用于安装
│   ├── pyqt6-xxx.whl
│   └── pyinstaller-xxx.whl
└── README.md             # 项目说明文档
```

---

## 版权声明

本项目版权归 Lemonsuqing 所有，未经授权禁止复制、传播。

---

## 如果你想请我喝一杯咖啡的话

<img src="assets/Please_buy_me_a_coffee.png" width="200">

---

# Water Reminder

A desktop water reminder application built with Python and PyQt6 to help you develop healthy hydration habits.

---

## Features

- Set fixed-time water reminders
- Customize reminder message
- Always-on-top popup reminders
- Runs in the system tray and supports background operation
- Supports building as a standalone `.exe` (no command window)

---

## Requirements

- Python 3.7 or higher

---

当然可以！下面是你的英文版 `README.md`，已完全翻译并保持原结构、术语与项目一致，同时保留了图像展示：

---

# Water Reminder

A desktop water reminder application built with Python and PyQt6 to help you develop healthy hydration habits.

---

## Features

- Set fixed-time water reminders
- Customize reminder message
- Always-on-top popup reminders
- Runs in the system tray and supports background operation
- Supports building as a standalone `.exe` (no command window)

---

## Requirements

- Python 3.7 or higher

---

## Installation & Usage

### 1. Install dependencies (if you want to run manually)

```bash
pip install PyQt6
````

### 2. Run the program (development environment)

```bash
pythonw main.py
```

> `pythonw` is recommended to avoid opening a command-line window.

---

### 3. One-click Build (Windows)

Double-click `build.cmd`. During the build process, the script will automatically check and install dependencies (`PyQt6`, `PyInstaller`), then generate a standalone executable.

Output executable location:

* Default: `WaterReminder.exe` in the current directory

---

## Clean Up Build Files

Run `Uninstall.cmd` to delete all intermediate build files and the generated `.exe` to keep your workspace clean.

---

## How to Use

1. Launch the program and choose a reminder interval
2. Set the reminder time
3. Enter a custom message (optional; default is "Time to drink water! Stay hydrated ❤️")
4. Click “Start Reminder”
5. The program will minimize to the system tray and show a popup at the set time
6. Right-click the tray icon to restore the window or exit the app

---

## Project Structure

```
├── assets/               # Icon assets
│   └── icon.ico          # Tray icon
├── build.cmd             # One-click build script
├── Uninstall.cmd         # One-click clean script
├── WaterReminder.exe     # Built executable
├── source/               # Python source files
│   ├── gui.py            # GUI logic
│   ├── main.py           # Application entry point
│   └── reminder.py       # Reminder logic
├── tool/                 # Wheel files for offline install
│   ├── pyqt6-xxx.whl
│   └── pyinstaller-xxx.whl
└── README.md             # Project documentation
```

---

## License

Copyright © 2025 Lemonsuqing
All rights reserved. Unauthorized reproduction or distribution is prohibited.

---

## If you'd like to buy me a coffee

<img src="assets/Please_buy_me_a_coffee.png" width="200">
```

---
