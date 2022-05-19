class GradingFormat:
    def __init__(self, g_id, desc, presentation_required, passing_grade):
        self.g_id = g_id
        self.desc = desc
        self.presentation_required = presentation_required
        self.passing_grade = passing_grade

    def __repr__(self):
        return str(self.__dict__)
