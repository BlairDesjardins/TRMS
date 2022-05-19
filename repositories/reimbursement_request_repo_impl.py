from models.event_type import EventType
from models.grading_format import GradingFormat
from util.db_connection import connection
from exceptions.resource_not_found import ResourceNotFound
from models.reimbursement_request import ReimbursementRequest, ApprovalStatus
from repositories.reimbursement_request_repo import ReimbursementRequestRepo


def _build_reimbursement_request(record):
    return ReimbursementRequest(r_id=int(record[0]), employee_id=int(record[1]) if record[1] else None,
                                approval_status=ApprovalStatus(record[2]), datetime=record[3], location=record[4],
                                desc=record[5], cost=float(record[6]), grading_id=int(record[7]) if record[7] else None,
                                event_type_id=int(record[8]) if record[8] else None)


class ReimbursementRequestRepoImpl(ReimbursementRequestRepo):
    def create_reimbursement_request(self, reimbursement_request):
        sql = "INSERT INTO reimbursement_requests VALUES (DEFAULT, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *"
        cursor = connection.cursor()

        cursor.execute(sql, [reimbursement_request.employee_id, reimbursement_request.approval_status,
                             reimbursement_request.datetime, reimbursement_request.location,
                             reimbursement_request.desc, reimbursement_request.cost,
                             reimbursement_request.grading_id, reimbursement_request.event_type_id])

        connection.commit()
        record = cursor.fetchone()

        return _build_reimbursement_request(record)

    def get_all_reimbursement_requests(self):
        sql = "SELECT * FROM reimbursement_requests"
        cursor = connection.cursor()

        cursor.execute(sql)

        records = cursor.fetchall()

        return [_build_reimbursement_request(record) for record in records]

    def get_reimbursement_request(self, reimbursement_request_id):
        sql = "SELECT * FROM reimbursement_requests WHERE r_id = %s"
        cursor = connection.cursor()

        cursor.execute(sql, [reimbursement_request_id])

        record = cursor.fetchone()
        if record:
            return _build_reimbursement_request(record)
        else:
            raise ResourceNotFound(f"Request with ID: {reimbursement_request_id} not found")

    def update_reimbursement_request(self, change):
        sql = "UPDATE reimbursement_requests " \
              'SET employee_id=%s, approval_status=%s, datetime=%s, location=%s, "desc"=%s, ' \
              "cost=%s, grading_id=%s, event_type_id=%s WHERE r_id=%s RETURNING *"
        cursor = connection.cursor()

        cursor.execute(sql, [change.employee_id, change.approval_status, change.datetime,
                             change.location, change.desc, change.cost,
                             change.grading_id, change.event_type_id, change.r_id])

        connection.commit()
        record = cursor.fetchone()
        if record:
            return _build_reimbursement_request(record)
        else:
            raise ResourceNotFound(f"Request with ID: {change.r_id} not found")

    def delete_reimbursement_request(self, reimbursement_request_id):
        sql = "DELETE FROM reimbursement_requests WHERE r_id=%s RETURNING *"
        cursor = connection.cursor()

        cursor.execute(sql, [reimbursement_request_id])

        connection.commit()
        record = cursor.fetchone()
        if record:
            return _build_reimbursement_request(record)
        else:
            raise ResourceNotFound(f"Request with ID: {reimbursement_request_id} not found")

    def get_all_event_types(self):
        sql = "SELECT * FROM event_types"
        cursor = connection.cursor()

        cursor.execute(sql)

        records = cursor.fetchall()

        return [EventType(e_id=record[0], name=record[1], reimbursement_coverage=record[2]) for record in records]

    def get_all_grading_formats(self):
        sql = "SELECT * FROM grading_formats"
        cursor = connection.cursor()

        cursor.execute(sql)

        records = cursor.fetchall()

        return [GradingFormat(g_id=record[0], desc=record[1], presentation_required=record[2],
                              passing_grade=record[3]) for record in records]

    def get_requests_for_super(self, employee_id):
        sql = "select * from reimbursement_requests left join employees on employee_id=e_id where super_id = %s and " \
              "approval_status = 0"
        cursor = connection.cursor()

        cursor.execute(sql, [employee_id])

        records = cursor.fetchall()

        return [_build_reimbursement_request(record) for record in records]

    def get_requests_for_dep_head(self, employee_id):
        sql = "select * from reimbursement_requests left join employees on employee_id=e_id left join departments on " \
              "dep_id=d_id where dep_head_id = %s and approval_status = 1"
        cursor = connection.cursor()

        cursor.execute(sql, [employee_id])

        records = cursor.fetchall()

        return [_build_reimbursement_request(record) for record in records]

    def get_requests_for_benco(self, employee_id):
        sql = "select * from departments where d_id=4 and dep_head_id=%s"
        cursor = connection.cursor()
        cursor.execute(sql, [employee_id])
        records = cursor.fetchall()

        if records:
            sql = "select * from reimbursement_requests where approval_status = 2"
            cursor = connection.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            return [_build_reimbursement_request(record) for record in records]
        else:
            return []

    def get_total_reimbursements_by_employee(self):
        sql = "select employee_id, sum(cost * reimbursement_coverage) from reimbursement_requests " \
              "left join event_types on event_type_id = e_id " \
              "where approval_status != -1 group by employee_id"
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()

        return [(record[0], float(record[1])) for record in records]


if __name__ == '__main__':
    rr = ReimbursementRequestRepoImpl()
    print(rr.get_total_reimbursements_by_employee())
