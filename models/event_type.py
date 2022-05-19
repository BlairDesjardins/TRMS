class EventType:
    def __init__(self, e_id, name, reimbursement_coverage):
        self.e_id = e_id
        self.name = name
        self.reimbursement_coverage = reimbursement_coverage

    def __repr__(self):
        return str(self.__dict__)
