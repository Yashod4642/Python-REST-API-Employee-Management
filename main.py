
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Employee Management API")


# 1. Database connection
def get_connection():
    connection = sqlite3.connect("employee.db")
    connection.row_factory = sqlite3.Row
    return connection


# 2. Employee model for POST and PUT
class Employee(BaseModel):
    id: int
    name: str
    email: str
    salary: float
    department: str


# 3. Employee model for PATCH
class EmployeeUpdate(BaseModel):
    name: str = None
    email: str = None
    salary: float = None
    department: str = None


# 4. GET - Retrieve all employees
@app.get("/employees")
def get_employees():

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT * FROM employees")
        records = cursor.fetchall()

        employees = [dict(row) for row in records]

        return employees

    finally:
        connection.close()


# 5. GET - Retrieve employee by ID
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT * FROM employees WHERE id = ?",
            (employee_id,)
        )

        record = cursor.fetchone()

        if record is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        return dict(record)

    finally:
        connection.close()


# 6. POST - Create a new employee
@app.post("/employees", status_code=201)
def create_employee(employee: Employee):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO employees
            (id, name, email, salary, department)
            VALUES (?, ?, ?, ?, ?)
        """, (
            employee.id,
            employee.name,
            employee.email,
            employee.salary,
            employee.department
        ))

        connection.commit()

        return {
            "message": "Employee created successfully",
            "employee": employee.model_dump()
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Employee ID or email already exists"
        )

    finally:
        connection.close()


# 7. PUT - Update complete employee details
@app.put("/employees/{employee_id}")
def replace_employee(employee_id: int, employee: Employee):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT * FROM employees WHERE id = ?",
            (employee_id,)
        )

        existing_employee = cursor.fetchone()

        if existing_employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        if employee.id != employee_id:
            raise HTTPException(
                status_code=400,
                detail="Employee ID in URL and body must match"
            )

        cursor.execute("""
            UPDATE employees
            SET name = ?,
                email = ?,
                salary = ?,
                department = ?
            WHERE id = ?
        """, (
            employee.name,
            employee.email,
            employee.salary,
            employee.department,
            employee_id
        ))

        connection.commit()

        cursor.execute(
            "SELECT * FROM employees WHERE id = ?",
            (employee_id,)
        )

        updated_employee = dict(cursor.fetchone())

        return {
            "message": "Employee updated successfully",
            "employee": updated_employee
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    finally:
        connection.close()


# 8. PATCH - Update selected employee fields
@app.patch("/employees/{employee_id}")
def update_employee(employee_id: int, employee: EmployeeUpdate):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT * FROM employees WHERE id = ?",
            (employee_id,)
        )

        existing_employee = cursor.fetchone()

        if existing_employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        update_data = employee.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided for update"
            )

        set_clause = ", ".join(
            f"{column} = ?" for column in update_data
        )

        values = list(update_data.values())
        values.append(employee_id)

        query = f"""
            UPDATE employees
            SET {set_clause}
            WHERE id = ?
        """

        cursor.execute(query, values)
        connection.commit()

        cursor.execute(
            "SELECT * FROM employees WHERE id = ?",
            (employee_id,)
        )

        updated_employee = dict(cursor.fetchone())

        return {
            "message": "Employee updated successfully",
            "employee": updated_employee
        }

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    finally:
        connection.close()


# 9. DELETE - Delete employee by ID
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "SELECT * FROM employees WHERE id = ?",
            (employee_id,)
        )

        existing_employee = cursor.fetchone()

        if existing_employee is None:
            raise HTTPException(
                status_code=404,
                detail="Employee not found"
            )

        cursor.execute(
            "DELETE FROM employees WHERE id = ?",
            (employee_id,)
        )

        connection.commit()

        return {
            "message": "Employee deleted successfully",
            "deleted_employee": dict(existing_employee)
        }

    finally:
        connection.close()
