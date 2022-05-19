from util.db_connection import connection
from exceptions.resource_not_found import ResourceNotFound
from models.employee import Employee
from repositories.employee_repo import EmployeeRepo


def _build_employee(record):
    return Employee(e_id=int(record[0]), first_name=record[1], last_name=record[2],
                    super_id=int(record[3]) if record[3] else None,
                    dep_id=int(record[4]) if record[4] else None,
                    email=record[5], password=record[6])


class EmployeeRepoImpl(EmployeeRepo):

    def create_employee(self, employee):
        sql = "INSERT INTO employees VALUES (DEFAULT, %s, %s, %s, %s, %s, %s) RETURNING *"
        cursor = connection.cursor()

        cursor.execute(sql, [employee.first_name, employee.last_name, employee.super_id, employee.dep_id,
                             employee.email, employee.password])

        connection.commit()
        record = cursor.fetchone()

        return _build_employee(record)

    def get_all_employees(self):
        sql = "SELECT * FROM employees"
        cursor = connection.cursor()

        cursor.execute(sql)

        records = cursor.fetchall()

        return [_build_employee(record) for record in records]

    def get_employee(self, employee_id):
        sql = "SELECT * FROM employees WHERE e_id = %s"
        cursor = connection.cursor()

        cursor.execute(sql, [employee_id])

        record = cursor.fetchone()
        if record:
            return _build_employee(record)
        else:
            raise ResourceNotFound(f"Employee with ID: {employee_id} not found")

    def update_employee(self, change):
        sql = "UPDATE employees SET fname=%s, lname=%s, super_id=%s, dep_id=%s, email=%s, password=%s " \
              "WHERE e_id=%s RETURNING *"
        cursor = connection.cursor()

        cursor.execute(sql, [change.first_name, change.last_name, change.super_id, change.dep_id,
                             change.email, change.password, change.e_id])

        connection.commit()
        record = cursor.fetchone()
        if record:
            return _build_employee(record)
        else:
            raise ResourceNotFound(f"Employee with ID: {change.e_id} not found")

    def delete_employee(self, employee_id):
        sql = "DELETE FROM employees WHERE e_id=%s RETURNING *"
        cursor = connection.cursor()

        cursor.execute(sql, [employee_id])

        connection.commit()
        record = cursor.fetchone()
        if record:
            return _build_employee(record)
        else:
            raise ResourceNotFound(f"Employee with ID: {employee_id} not found")
