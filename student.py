import os, pickle
from db import mycur,mydb
from libs.fuzzywuzzy import fuzz
from libs.fuzzywuzzy import process
from utils import *
import random, time
from mail import *
from libs.rich.table import Table
from libs.rich.console import Console

os.system('cls')
print()
print()
console.print("[red]LIPS Library Management System[/red]", justify="center",)

print("Select an Option:")
print("1. [green]Check Availability")
print("2. [green]Reserve A Book")
print("3. [green]Update E-Mail")
print("4. [green]Recieve Library Card")
print("5. [green]Pay Fine")
print("6. [green]Exit")

ch = input(">")

if ch == "1":
	while True:
		id, binfo = book_check()
		print_book(binfo)
		if binfo[4] != 0: 		
			print("The Book is not available")
		else:
			print("The Book is Available")
elif ch == "2":
	while True:
		bs = input("Enter Book Name or Book ID >> ")
		if bs.isnumeric():
			mycur.execute(f"SELECT * FROM BOOKS WHERE ID = {bs}")
			binfo = mycur.fetchone()
			if binfo == None:
				print("Book Does Not Exists!")
		else:
			mycur.execute("SELECT * FROM BOOKS")
			bdb = mycur.fetchall()
			table = Table(show_header=True, header_style="bold magenta")
			table.add_column("ID", style="dim", width=12)
			table.add_column("Title")
			table.add_column("Author", justify="right")
			table.add_column("Price", justify="right")
			table.add_column("Issued To", justify="right")
			table.add_column("Issued Date", justify="right")
			table.add_column("Is Reserved?", justify="right")
			l1 = []
			for i in bdb:
				if fuzz.ratio(bs.lower(), i[1].lower()) > 60:
					if i[4] != 0:
						name = "Issued"
					else:
						name = "Not Issued"
					if i[6] != 0:
						nameR = "Reserved"
					else:
						nameR = "Not Reserved"
					l1.append([i[0], i[1], i[2], i[3], name, i[5],nameR])
					table.add_row("[cyan]" + str(i[0]), "[green]" + str(i[1]), "[green]" + str(i[2]),"[green]" + str(i[3]), "[green]" + name, "[green]" + str(i[5]), "[green]", nameR)
			if len(l1) == 0:
				binfo = None
				print("No Result Found")
			else:
				console.print(table)
				id, binfo = book_check()
		if binfo != None:
			break
	
	print_book(binfo)
	if binfo[6] == 0:
		if binfo[4] != 0: 		
			print("The Book is not available")
		else:
			print("The Book is Available")
			with open("data.pickle", "rb") as f:
				data = pickle.load(f)
			mycur.execute(f"SELECT * FROM BOOKS WHERE RESERVED = {data[0]}")
			if len(mycur.fetchall()) > 2:
				print("You Reached The Maximum Limit to Issue Books")
			else:
				if input("Do You Want to Reserve This Book? (y/n)") not in ("n", "nn", "not"):
					mycur.execute(f"UPDATE BOOKS SET RESERVED = {data[0]} WHERE ID = {binfo[0]}")
					mydb.commit()
					print("Your Book has been reserved")
	else:
		print("The Book is Already Reserved")
elif ch == "3":
	while True:
		while True:
			emailid = input("Enter New E-Mail ID")
			if emailid == "exit":
				exit()
			if check_email(emailid):
				break
		echeck = mycur.execute(f"SELECT * FROM ACCOUNTS WHERE EMAIL = '{emailid}'")
		if mycur.fetchone() != None:
			print("Email Already Exists! Try again.")
		else:
			break	
	code = random.randint(100000,999999)
	with open("data.pickle", "rb") as f:
		data = pickle.load(f)
		username = data[2]
	if check_internet():
		send_verify(emailid,code,username)
		while True:
			if input("Enter OTP > ") == str(code):
				mycur.execute(f"UPDATE ACCOUNTS SET EMAIL = '{emailid}' WHERE ID = {data[0]}")
				mydb.commit()
				print("EMail ID Updated Successfully")
				break
			else:
				print("Try Again")
	else:
		print("Please Connect To Internet")
elif ch == "4":
	with open("data.pickle", "rb") as f:
		data = pickle.load(f)
	generate_pdf(data[2],data[2], data[5])
	print("Library Card Saved on your Current Folder")

elif ch == "5":
	with open("data.pickle", "rb") as f:
		data = pickle.load(f)
	mycur.execute(f"SELECT * FROM ACCOUNTS WHERE ID = {data[0]}")
	data = mycur.fetchone()
	print("Your Total Fine Ammount is Rs. ", data[4])
	print("Select An Option")
	print("1. Create Payment")
	print("2. Verify Payment")
	chchch = input(">> ")
	if chchch == "1":
		if data[4] > 0:
			time.sleep(3)
			linkid = str(int(time.time()))+str(data[0])
			ammount = data[4]
			note = "Fine Payment of "+ data[2]
			print("Generating Link Please Wait...")
			try:
				data2 = generate_payment(input("Enter Mobile Number>>"), linkid,int(ammount),note)
				mycur.execute(f"UPDATE ACCOUNTS SET LINKID = '{linkid}' WHERE ID = {data[0]}")
				mydb.commit()
				os.system("start "+data2['link_url'])
			except:
				print("An Error Occured While Creating Payment Link")
	elif chchch == "2":
		with open("data.pickle", "rb") as f:
			uid = pickle.load(f)[0]
		mycur.execute(f"SELECT * FROM ACCOUNTS WHERE ID = {uid}")
		data = mycur.fetchone()
		linkid = data[6]
		if linkid != None:
			if verify_payment(linkid)["link_status"] == "PAID":
				mycur.execute(f"UPDATE ACCOUNTS SET AMMOUNT = 0, LINKID = Null WHERE ID = '{uid}'")
				mydb.commit()
				print("The Payment was successfull! Your Fine has been set to 0")
			else:
				print("The Payment was Not Successfull. If Any Error. Contact Admin")
		else:
			print("No Payment Link Created")
elif ch == "6":
	exit()
time.sleep(5)