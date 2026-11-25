
import sqlite3

connection = sqlite3.connect("employee.db")
cursor = connection.cursor()

cursor.execute("""
DELETE FROM employees
WHERE id = 103
""")

connection.commit()

print("Employee deleted successfully!")

connection.close()
