.PHONY: build clean

# 可执行文件名称
EXE_NAME = WaterReminder

build:
	pyinstaller --noconsole --onefile --add-data "assets/icon.ico;assets" --name $(EXE_NAME) main.py

clean:
	rm -rf build dist __pycache__ $(EXE_NAME).spec
