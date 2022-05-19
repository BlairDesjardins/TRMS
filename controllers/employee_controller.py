from flask import jsonify, request

from exceptions.resource_not_found import ResourceNotFound
from exceptions.unauthorized import Unauthorized
from models.employee import Employee
from repositories.employee_repo_impl import EmployeeRepoImpl
from services.employee_service import EmployeeService
from util.json_conversion import to_json

er = EmployeeRepoImpl()
es = EmployeeService(er)


def route(app):

    @app.route("/employees", methods=['GET'])
    def get_all_employees():
        return jsonify([to_json(employee) for employee in es.get_all_employees()])

    @app.route("/employees/<employee_id>", methods=['GET'])
    def get_employee(employee_id):
        try:
            return to_json(es.get_employee(int(employee_id)))
        except ValueError:
            return "Not a valid ID", 400
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/employees", methods=['POST'])
    def create_employee():
        body = request.json

        employee = es.create_employee(Employee(
            first_name=body["firstName"],
            last_name=body["lastName"],
            super_id=body["superId"],
            dep_id=body["depId"],
            email=body["email"],
            password=body["password"]
        ))

        return to_json(employee), 201

    @app.route("/employees/<employee_id>", methods=['PUT'])
    def update_employee(employee_id):
        try:
            body = request.json

            employee = es.update_employee(Employee(
                e_id=employee_id,
                first_name=body["firstName"],
                last_name=body["lastName"],
                super_id=body["superId"],
                dep_id=body["depId"],
                email=body["email"],
                password=body["password"]
            ))

            return to_json(employee)
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/employees/<employee_id>", methods=['DELETE'])
    def delete_employee(employee_id):
        try:
            es.delete_employee(employee_id)
            return '', 204
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/employees/login", methods=['POST'])
    def login():
        try:
            body = request.json
            employee = es.login_employee(body["email"], body["password"])
            return to_json(employee)
        except Unauthorized as e:
            return e.message, 401
