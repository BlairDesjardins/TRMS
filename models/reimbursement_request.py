from enum import Enum


class ApprovalStatus(int, Enum):
    REJECTED = -1
    NO_APPROVAL = 0
    SUPER_APPROVAL = 1
    DEP_HEAD_APPROVAL = 2
    BENCO_APPROVAL = 3


class ReimbursementRequest:

    def __init__(self, r_id=0, employee_id=None, approval_status=ApprovalStatus.NO_APPROVAL, datetime=0,
                 location="", desc="", cost=0, grading_id=None, event_type_id=None):
        self.r_id = r_id
        self.employee_id = employee_id
        self.approval_status = approval_status
        self.datetime = datetime
        self.location = location
        self.desc = desc
        self.cost = cost
        self.grading_id = grading_id
        self.event_type_id = event_type_id

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__