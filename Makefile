dev:
	fastapi dev main.py

run:
	fastapi run main.py

bin:
	pyinstaller -F main.py --hidden-import passlib.handlers.bcrypt --optimize 2