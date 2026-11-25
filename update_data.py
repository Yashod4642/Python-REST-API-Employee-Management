
import sqlite3

connection = sqlite3.connect("employee.db")
cursor = connection.cursor()

cursor.execute("""
UPDATE employees
SET salary = 45000
WHERE id = 101
""")

connection.commit()

print("Employee salary updated successfully!")

connection.close()
