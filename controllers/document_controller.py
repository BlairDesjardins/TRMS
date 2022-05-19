from flask import jsonify, request

from exceptions.resource_not_found import ResourceNotFound
from models.document import Document
from repositories.document_repo_impl import DocumentRepoImpl
from services.document_service import DocumentService
from util.json_conversion import to_json

dr = DocumentRepoImpl()
ds = DocumentService(dr)


def route(app):

    @app.route("/documents", methods=['GET'])
    def get_all_documents():
        return jsonify([to_json(employee) for employee in ds.get_all_documents()])

    @app.route("/documents/<document_id>", methods=['GET'])
    def get_document(document_id):
        try:
            return to_json(ds.get_document(int(document_id)))
        except ValueError:
            return "Not a valid ID", 400
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/documents", methods=['POST'])
    def create_document():
        body = request.json

        document = ds.create_document(Document(
            desc=body["desc"],
            request_id=body["requestId"],
            grade=body["grade"]
        ))

        return to_json(document), 201

    @app.route("/documents/<document_id>", methods=['PUT'])
    def update_document(document_id):
        try:
            body = request.json

            document = ds.update_document(Document(
                d_id=document_id,
                desc=body["desc"],
                request_id=body["requestId"],
                grade=body["grade"]
            ))

            return to_json(document)
        except ValueError:
            return "Not a valid ID", 400
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/documents/<document_id>", methods=['DELETE'])
    def delete_document(document_id):
        try:
            ds.delete_document(document_id)
            return '', 204
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/requests/<request_id>/documents", methods=['GET'])
    def get_documents_for_request(request_id):
        try:
            return jsonify([to_json(doc) for doc in ds.get_documents_for_request(int(request_id))])
        except ValueError:
            return "Not a valid ID", 400
        except ResourceNotFound as r:
            return r.message, 404
