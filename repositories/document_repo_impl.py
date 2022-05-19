from util.db_connection import connection
from exceptions.resource_not_found import ResourceNotFound
from models.document import Document
from repositories.document_repo import DocumentRepo


def _build_document(record):
    return Document(d_id=int(record[0]), desc=record[1], request_id=int(record[2]) if record[2] else None,
                    grade=float(record[3]))


class DocumentRepoImpl(DocumentRepo):
    def create_document(self, document):
        sql = "INSERT INTO documents VALUES (DEFAULT, %s, %s, %s) RETURNING *"
        cursor = connection.cursor()

        cursor.execute(sql, [document.desc, document.request_id, document.grade])

        connection.commit()
        record = cursor.fetchone()

        return _build_document(record)

    def get_all_documents(self):
        sql = "SELECT * FROM documents"
        cursor = connection.cursor()

        cursor.execute(sql)

        records = cursor.fetchall()

        return [_build_document(record) for record in records]

    def get_document(self, document_id):
        sql = "SELECT * FROM documents WHERE d_id = %s"
        cursor = connection.cursor()

        cursor.execute(sql, [document_id])

        record = cursor.fetchone()
        if record:
            return _build_document(record)
        else:
            raise ResourceNotFound(f"Document with ID: {document_id} not found")

    def update_document(self, change):
        sql = 'UPDATE documents SET "desc"=%s, request_id=%s, grade=%s WHERE d_id=%s RETURNING *'
        cursor = connection.cursor()

        cursor.execute(sql, [change.desc, change.request_id, change.grade, change.d_id])

        connection.commit()
        record = cursor.fetchone()
        if record:
            return _build_document(record)
        else:
            raise ResourceNotFound(f"Document with ID: {change.d_id} not found")

    def delete_document(self, document_id):
        sql = "DELETE FROM documents WHERE d_id=%s RETURNING *"
        cursor = connection.cursor()

        cursor.execute(sql, [document_id])

        connection.commit()
        record = cursor.fetchone()
        if record:
            return _build_document(record)
        else:
            raise ResourceNotFound(f"Document with ID: {document_id} not found")


def _test():
    repo = DocumentRepoImpl()

    # repo.create_document(Document(desc="Doc desc", request_id=3, grade=77))

    print(repo.get_all_documents())
    # repo.update_document(Document(d_id=4, desc="Doc desc 2", request_id=3, grade=77))
    repo.delete_document(1)
    print(repo.get_document(1))


if __name__ == '__main__':
    _test()
