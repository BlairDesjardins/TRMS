from flask import jsonify, request

from exceptions.resource_not_found import ResourceNotFound
from exceptions.resource_unavailable import ResourceUnavailable
from models.reimbursement_request import ReimbursementRequest
from repositories.reimbursement_request_repo_impl import ReimbursementRequestRepoImpl
from services.reimburse_request_service import ReimbursementRequestService
from util.json_conversion import to_json

rr = ReimbursementRequestRepoImpl()
rs = ReimbursementRequestService(rr)


def route(app):

    @app.route("/requests", methods=['GET'])
    def get_all_requests():
        return jsonify([to_json(r_request) for r_request in rs.get_all_reimbursement_requests()])

    @app.route("/requests/<request_id>", methods=['GET'])
    def get_request(request_id):
        try:
            return to_json(rs.get_reimbursement_request(int(request_id)))
        except ValueError:
            return "Not a valid ID", 400
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/requests", methods=['POST'])
    def create_request():
        try:
            body = request.json

            r_request = rs.create_reimbursement_request(ReimbursementRequest(
                employee_id=body["employeeId"],
                approval_status=body["approvalStatus"],
                datetime=body["datetime"],
                location=body["location"],
                desc=body["desc"],
                cost=body["cost"],
                grading_id=body["gradingId"],
                event_type_id=body["eventTypeId"]
            ))

            return to_json(r_request), 201
        except ResourceUnavailable as r:
            return r.message, 422

    @app.route("/requests/<request_id>", methods=['PUT'])
    def update_request(request_id):
        try:
            body = request.json

            r_request = rs.update_reimbursement_request(ReimbursementRequest(
                r_id=request_id,
                employee_id=body["employeeId"],
                approval_status=body["approvalStatus"],
                datetime=body["datetime"],
                location=body["location"],
                desc=body["desc"],
                cost=body["cost"],
                grading_id=body["gradingId"],
                event_type_id=body["eventTypeId"]
            ))

            return to_json(r_request)
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/requests/<request_id>", methods=['DELETE'])
    def delete_request(request_id):
        try:
            rs.delete_reimbursement_request(request_id)
            return '', 204
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/requests/<request_id>", methods=['PATCH'])
    def change_approval_status(request_id):
        body = request.json

        try:
            if "status" in body:
                r = rs.update_request_approval(request_id, body["status"])
                return to_json(r)
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/employees/<employee_id>/requests", methods=['GET'])
    def get_requests_for_employee(employee_id):
        requests = []
        admin = request.args.get("admin", type=bool)
        if admin:
            requests += [to_json(r_request) for r_request in rs.get_requests_for_super(int(employee_id))]
            requests += [to_json(r_request) for r_request in rs.get_requests_for_dep_head(int(employee_id))]
            requests += [to_json(r_request) for r_request in rs.get_requests_for_benco(int(employee_id))]
        else:
            requests += [to_json(r_request) for r_request in rs.get_requests_for_employee(int(employee_id))]
        if len(requests) > 0:
            return jsonify(requests)
        else:
            return f"No requests found for employee with ID: {employee_id}", 404

    @app.route("/events", methods=['GET'])
    def get_event_type():
        return jsonify([to_json(event) for event in rs.get_all_event_types()])

    @app.route("/formats", methods=['GET'])
    def get_grading_formats():
        return jsonify([to_json(event) for event in rs.get_all_grading_formats()])
