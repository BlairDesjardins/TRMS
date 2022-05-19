from abc import ABC, abstractmethod


class DocumentRepo(ABC):

    @abstractmethod
    def create_document(self, document):
        pass

    @abstractmethod
    def get_all_documents(self):
        pass

    @abstractmethod
    def get_document(self, document_id):
        pass

    @abstractmethod
    def update_document(self, change):
        pass

    @abstractmethod
    def delete_document(self, document_id):
        pass
