from exceptions.resource_not_found import ResourceNotFound
from repositories.document_repo import DocumentRepo


class DocumentService:

    def __init__(self, document_repo: DocumentRepo):
        self.document_repo = document_repo

    def create_document(self, document):
        return self.document_repo.create_document(document)

    def get_all_documents(self):
        return self.document_repo.get_all_documents()

    def get_document(self, document_id):
        return self.document_repo.get_document(document_id)

    def update_document(self, change):
        return self.document_repo.update_document(change)

    def delete_document(self, document_id):
        return self.document_repo.delete_document(document_id)

    def get_documents_for_request(self, request_id):
        all_docs = self.document_repo.get_all_documents()
        results = list(filter(lambda d: (d.request_id == request_id), all_docs))
        if len(results) != 0:
            return results
        else:
            raise ResourceNotFound(f"Request with ID: {request_id} not found or does not have any requests")
