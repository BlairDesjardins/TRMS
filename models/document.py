class Document:

    def __init__(self, d_id=0, desc="", request_id=None, grade=0):
        self.d_id = d_id
        self.desc = desc
        self.request_id = request_id
        self.grade = grade

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__