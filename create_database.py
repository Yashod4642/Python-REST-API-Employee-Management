
import sqlite3

connection = sqlite3.connect("employee.db")
cursor = connection.cursor()

# Insert employee records
cursor.execute("""
INSERT INTO employees (id, name, email, salary, department)
VALUES (101, 'Ravi', 'ravi@gmail.com', 30000, 'Testing')
""")

cursor.execute("""
INSERT INTO employees (id, name, email, salary, department)
VALUES (102, 'Kumar', 'kumar@gmail.com', 40000, 'Development')
""")

cursor.execute("""
INSERT INTO employees (id, name, email, salary, department)
VALUES (103, 'Priya', 'priya@gmail.com', 35000, 'Testing')
""")

connection.commit()

print("Employee records inserted successfully!")

connection.close()
