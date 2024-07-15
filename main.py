from login import *
import pickle, os

from rich.console import Console
console = Console()

if os.path.exists("data.pickle"):
	with open("data.pickle","rb") as f:
		data = pickle.load(f)
		
		if data[1] == "A":
			os.system("python admin.py")
		elif data[1] == "S":
			os.system("python student.py")
else:
	print("Select Your Choice: ")
	print("1. Admin")
	print("2. Student")
	choice = input(">>")
	if choice == "1":
		admin_login_func()
	else:
		student_login_func()