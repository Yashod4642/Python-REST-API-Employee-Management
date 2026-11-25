
import sqlite3

connection = sqlite3.connect("employee.db")
cursor = connection.cursor()

cursor.execute("SELECT * FROM employees")

records = cursor.fetchall()

for row in records:
    print(row)

connection.close()
