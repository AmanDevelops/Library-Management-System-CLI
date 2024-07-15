import os
from db import mycur, mydb
import pickle
import hashlib
from mail import *
import random
from utils import check_email

os.system('cls')

def admin_login_func():
	print("Welcome To Library Management System\n")
	mycur.execute("SELECT * FROM ACCOUNTS WHERE TYPE = 'A'")
	ldta = mycur.fetchone()
	fpass = ldta[3]
	login = False
	while login != True:
		password = input("Enter Your password : ")
		if hashlib.md5(password.encode()).hexdigest() == fpass:
			print("Logged in Successfully! ")
			break
		else:
			print("Auth Unsuccessfull!")
	with open("data.pickle", "wb") as f:
		pickle.dump(ldta,f)
	os.system("cls")

def student_login_func():
	print("Welcome To Library Management System\n")
	print("Select Your Option")
	print("1. Signup")
	print("2. Login")
	print("3. Reset Password")
	ch = input("> ")
	if ch == "1":
		while True:
			uname = input("Enter Your Username : ")
			ucheck = mycur.execute(f"SELECT * FROM ACCOUNTS WHERE USERNAME = '{uname}'")
			if mycur.fetchone() != None:
				print("Username Already Exists! Try again.")
			else:
				break
		while True:
			while True:
				eml = input("Enter New E-Mail ID")
				if check_email(eml):
					break
			echeck = mycur.execute(f"SELECT * FROM ACCOUNTS WHERE EMAIL = '{eml}'")
			if mycur.fetchone() != None:
				print("Email Already Exists! Try again.")
			else:
				break

		password = hashlib.md5(input("Enter Your password : ").encode()).hexdigest()
		code = random.randint(100000,999999)
		try:
			send_verify(eml,code,uname)
		except:
			print("Connect To Internet and Try Again")
			exit()
		while True:
			if int(input("Enter Your Code >> ")) == code:
				mycur.execute(f"INSERT INTO ACCOUNTS (TYPE,USERNAME,PASSWORD,EMAIL) VALUES('S','{uname}','{password}','{eml}')")
				mydb.commit()
				print("Account Created Successfully! ")
				mycur.execute(f"SELECT * FROM ACCOUNTS WHERE USERNAME = '{uname}'")
				ldta = mycur.fetchone()
				send_reg(ldta[5],ldta[2], ldta[0])
				break
	if ch == "2":
		while True:
			uname = input("Enter Your Username : ")
			ucheck = mycur.execute(f"SELECT * FROM ACCOUNTS WHERE USERNAME = '{uname}'")
			if mycur.fetchone() == None:
				print("No Username Found! Try Again")
			else:
				break
		while True:
			password = hashlib.md5(input("Enter Your password : ").encode()).hexdigest()
			mycur.execute(f"SELECT * FROM ACCOUNTS WHERE USERNAME = '{uname}' AND PASSWORD = '{password}'")
			ldta = mycur.fetchone()
			if ldta != None:
				print("Logged in Successfully!")
				break
			else:
				print("Try Again")
	if ch == "3":
		while True:
			uname = input("Enter Your Username : ")
			ucheck = mycur.execute(f"SELECT * FROM ACCOUNTS WHERE USERNAME = '{uname}'")
			sdata = ucheck.fetchone()
			if sdata == None:
				print("No Username Found! Try Again")
			else:
				break
		code = random.randint(100000,999999)
		send_reset(sdata[5],code,uname)
		while True:
			if int(input("Enter Your Code >> ")) == code:
				password = hashlib.md5(input("Enter Your New password : ").encode()).hexdigest()
				mycur.execute(f"UPDATE ACCOUNTS SET PASSWORD = '{password}' WHERE USERNAME = '{uname}'")
				mydb.commit()
				print("Password Changed Successfully! ")
				mycur.execute(f"SELECT * FROM ACCOUNTS WHERE USERNAME = '{uname}'")
				ldta = mycur.fetchone()
				break
	with open("data.pickle", "wb") as f:
		pickle.dump(ldta,f)