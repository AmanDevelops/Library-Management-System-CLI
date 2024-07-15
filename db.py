import libs.mysql.connector

mydb = mysql.connector.connect(host="DATABASE_URL", user="DATABASE_USERNAME", password="DATABASE_PASSWORD", database="DATABASE_NAME")
mycur = mydb.cursor()


mycur.execute("UPDATE ACCOUNTS SET AMMOUNT = 500 WHERE ID = 3")
mydb.commit()

mycur.execute("SELECT * FROM ACCOUNTS")
data = mycur.fetchall()
for i in data:
	print(i)