class Employee:

    def __init__(self, e_id=0, first_name="", last_name="", super_id=None, dep_id=None, email="", password=""):
        self.e_id = e_id
        self.first_name = first_name
        self.last_name = last_name
        self.super_id = super_id
        self.dep_id = dep_id
        self.email = email
        self.password = password

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
