.PHONY: build clean

# 可执行文件名称
EXE_NAME = WaterReminder
CLOCK_NAME = ClassOver

build:
	pyinstaller --noconsole --onefile --add-data "assets/icon.ico;assets" --name $(EXE_NAME) main.py

clock_out:
	pyinstaller --noconsole --onefile --add-data "assets/1.ico;assets" --name $(CLOCK_NAME) clock_out_reminder.py

clean:
	rm -rf build dist __pycache__ $(EXE_NAME).spec $(CLOCK_NAME).spec
