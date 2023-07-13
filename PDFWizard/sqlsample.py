import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123ajinkya123",
  database='company'
)


mycursor = mydb.cursor()

insert_query = "INSERT INTO PDF (ID, Name, DateCreated, Content) VALUES (%s, %s, %s, %s)"
values = (103, 'PDF3', '2023-01-12', 'Content for PDF3')

mycursor.execute(insert_query, values)
mydb.commit()

# mycursor.execute("INSERT INTO VALUES(103, 'PDF3', 2023-01-12', 'Content for PDF3')")
mycursor.execute("SELECT * FROM PDF")


for x in mycursor:
  print(x)