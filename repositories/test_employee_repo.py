import unittest

from models.employee import Employee
from repositories.employee_repo_impl import EmployeeRepoImpl

er = EmployeeRepoImpl()


class TestEmployeeRepo(unittest.TestCase):
    added_employee = Employee()

    def test_1_create_employee_success(self):
        TestEmployeeRepo.added_employee = er.create_employee(self.added_employee)

        self.assertEqual(self.added_employee, Employee(e_id=self.added_employee.e_id, first_name="",
                                                       last_name="", super_id=None, dep_id=None,
                                                       email="", password=""))

    def test_2_read_employee_success(self):
        self.assertEqual(er.get_employee(self.added_employee.e_id),
                         Employee(e_id=self.added_employee.e_id, first_name="",
                                  last_name="", super_id=None, dep_id=None,
                                  email="", password=""))

    def test_3_update_employee_success(self):
        TestEmployeeRepo.added_employee = er.update_employee(Employee(e_id=self.added_employee.e_id, first_name="new",
                                                                      last_name="", super_id=None, dep_id=None,
                                                                      email="", password=""))
        self.assertEqual(self.added_employee.first_name, "new")

    def test_4_delete_employee_success(self):
        self.assertIsNotNone(er.delete_employee(self.added_employee.e_id))


if __name__ == '__main__':
    unittest.main(failfast=True, exit=False)
