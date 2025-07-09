.PHONY: build clean

# 可执行文件名称（你可以改成你想要的名字）
EXE_NAME = WaterReminder

build:
	pyinstaller --noconsole --onefile --name $(EXE_NAME) main.py

clean:
	rm -rf build dist __pycache__ $(EXE_NAME).spec
