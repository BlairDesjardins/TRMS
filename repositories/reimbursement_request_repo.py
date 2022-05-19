from abc import ABC, abstractmethod


class ReimbursementRequestRepo(ABC):

    @abstractmethod
    def create_reimbursement_request(self, reimbursement_request):
        pass

    @abstractmethod
    def get_all_reimbursement_requests(self):
        pass

    @abstractmethod
    def get_reimbursement_request(self, reimbursement_request_id):
        pass

    @abstractmethod
    def update_reimbursement_request(self, change):
        pass

    @abstractmethod
    def delete_reimbursement_request(self, reimbursement_request_id):
        pass

    @abstractmethod
    def get_all_event_types(self):
        pass

    @abstractmethod
    def get_all_grading_formats(self):
        pass

    @abstractmethod
    def get_requests_for_super(self, employee_id):
        pass

    @abstractmethod
    def get_requests_for_dep_head(self, employee_id):
        pass

    @abstractmethod
    def get_requests_for_benco(self, employee_id):
        pass

    @abstractmethod
    def get_total_reimbursements_by_employee(self):
        pass
