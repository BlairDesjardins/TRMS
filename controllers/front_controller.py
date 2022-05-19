from controllers import employee_controller, reimbursement_request_controller, document_controller


def route(app):
    employee_controller.route(app)
    reimbursement_request_controller.route(app)
    document_controller.route(app)
