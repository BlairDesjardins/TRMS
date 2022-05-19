from exceptions.unauthorized import Unauthorized
from repositories.employee_repo import EmployeeRepo
from repositories.employee_repo_impl import EmployeeRepoImpl


class EmployeeService:

    def __init__(self, employee_repo: EmployeeRepo):
        self.employee_repo = employee_repo

    def create_employee(self, employee):
        return self.employee_repo.create_employee(employee)

    def get_all_employees(self):
        return self.employee_repo.get_all_employees()

    def get_employee(self, employee_id):
        return self.employee_repo.get_employee(employee_id)

    def update_employee(self, change):
        return self.employee_repo.update_employee(change)

    def delete_employee(self, employee_id):
        return self.employee_repo.delete_employee(employee_id)

    def login_employee(self, email, password):
        all_employees = self.employee_repo.get_all_employees()
        result = list(filter(lambda e: (e.email == email and e.password == password), all_employees))
        if len(result) != 0:
            return result[0]
        else:
            raise Unauthorized(f"The email or password is incorrect")


def _test():
    er = EmployeeRepoImpl()
    es = EmployeeService(er)

    es.login_employee("jerry@email.com", "passwordlol")
    es.login_employee("jerry@email.com", "123")


if __name__ == '__main__':
    _test()
