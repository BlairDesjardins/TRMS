from abc import ABC, abstractmethod


class EmployeeRepo(ABC):

    @abstractmethod
    def create_employee(self, employee):
        pass

    @abstractmethod
    def get_all_employees(self):
        pass

    @abstractmethod
    def get_employee(self, employee_id):
        pass

    @abstractmethod
    def update_employee(self, change):
        pass

    @abstractmethod
    def delete_employee(self, employee_id):
        pass
