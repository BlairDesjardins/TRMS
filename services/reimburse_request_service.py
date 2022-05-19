from exceptions.resource_unavailable import ResourceUnavailable
from models.reimbursement_request import ReimbursementRequest
from repositories.reimbursement_request_repo import ReimbursementRequestRepo
from repositories.reimbursement_request_repo_impl import ReimbursementRequestRepoImpl


class ReimbursementRequestService:

    def __init__(self, reimbursement_request_repo: ReimbursementRequestRepo):
        self.reimbursement_request_repo = reimbursement_request_repo

    def create_reimbursement_request(self, reimbursement_request: ReimbursementRequest):
        available = 1000 - self.get_total_reimbursements_for_employee(reimbursement_request.employee_id)
        if available <= 0:
            raise ResourceUnavailable(f"You have reached the total amount of reimbursement money.")

        coverage = float(self.get_all_event_types()[int(reimbursement_request.event_type_id)-1].reimbursement_coverage)
        if (float(reimbursement_request.cost) * coverage) > available:
            reimbursement_request.cost = available / coverage

        return self.reimbursement_request_repo.create_reimbursement_request(reimbursement_request)

    def get_all_reimbursement_requests(self):
        return self.reimbursement_request_repo.get_all_reimbursement_requests()

    def get_reimbursement_request(self, reimbursement_request_id):
        return self.reimbursement_request_repo.get_reimbursement_request(reimbursement_request_id)

    def update_reimbursement_request(self, change):
        return self.reimbursement_request_repo.update_reimbursement_request(change)

    def delete_reimbursement_request(self, reimbursement_request_id):
        return self.reimbursement_request_repo.delete_reimbursement_request(reimbursement_request_id)

    def update_request_approval(self, reimbursement_request_id, status):
        request: ReimbursementRequest = self.get_reimbursement_request(reimbursement_request_id)
        request.approval_status = status
        self.update_reimbursement_request(request)
        return request

    def get_requests_for_employee(self, employee_id):
        all_requests = self.reimbursement_request_repo.get_all_reimbursement_requests()
        results = list(filter(lambda r: (r.employee_id == employee_id), all_requests))

        return results

    def get_all_event_types(self):
        return self.reimbursement_request_repo.get_all_event_types()

    def get_all_grading_formats(self):
        return self.reimbursement_request_repo.get_all_grading_formats()

    def get_requests_for_super(self, employee_id):
        return self.reimbursement_request_repo.get_requests_for_super(employee_id)

    def get_requests_for_dep_head(self, employee_id):
        return self.reimbursement_request_repo.get_requests_for_dep_head(employee_id)

    def get_requests_for_benco(self, employee_id):
        return self.reimbursement_request_repo.get_requests_for_benco(employee_id)

    def get_total_reimbursements_for_employee(self, employee_id):
        all_results = self.reimbursement_request_repo.get_total_reimbursements_by_employee()
        filtered = (list(filter(lambda r: (r[0] == int(employee_id)), all_results)))
        if len(filtered) > 0:
            e_id, total = filtered[0]
            return total
        return 0


if __name__ == '__main__':
    rr = ReimbursementRequestRepoImpl()
    rs = ReimbursementRequestService(rr)
    rs.get_total_reimbursements_for_employee(20)
