import unittest

from models.reimbursement_request import ReimbursementRequest, ApprovalStatus
from repositories.reimbursement_request_repo_impl import ReimbursementRequestRepoImpl

rr = ReimbursementRequestRepoImpl()


class TestRequestRepo(unittest.TestCase):
    added_request = ReimbursementRequest()

    def test_1_create_request_success(self):
        TestRequestRepo.added_request = rr.create_reimbursement_request(self.added_request)

        self.assertEqual(self.added_request, ReimbursementRequest(r_id=self.added_request.r_id, employee_id=None,
                                                                  approval_status=ApprovalStatus.NO_APPROVAL,
                                                                  datetime=0, location="", desc="",
                                                                  cost=0, grading_id=None,
                                                                  event_type_id=None))

    def test_2_read_request_success(self):
        self.assertEqual(rr.get_reimbursement_request(self.added_request.r_id),
                         ReimbursementRequest(r_id=self.added_request.r_id, employee_id=None,
                                              approval_status=ApprovalStatus.NO_APPROVAL,
                                              datetime=0, location="", desc="",
                                              cost=0, grading_id=None,
                                              event_type_id=None))

    def test_3_update_request_success(self):
        TestRequestRepo.added_request = rr.update_reimbursement_request(
            ReimbursementRequest(r_id=self.added_request.r_id, employee_id=None,
                                 approval_status=ApprovalStatus.SUPER_APPROVAL,
                                 datetime=0, location="", desc="",
                                 cost=0, grading_id=None,
                                 event_type_id=None))

        self.assertEqual(self.added_request.approval_status, ApprovalStatus.SUPER_APPROVAL)

    def test_4_delete_request_success(self):
        self.assertIsNotNone(rr.delete_reimbursement_request(self.added_request.r_id))


if __name__ == '__main__':
    unittest.main(failfast=True, exit=False)
