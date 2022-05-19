import unittest

from models.document import Document
from repositories.document_repo_impl import DocumentRepoImpl

dr = DocumentRepoImpl()


class TestDocumentRepo(unittest.TestCase):
    added_doc = Document()

    def test_1_create_request_success(self):
        TestDocumentRepo.added_doc = dr.create_document(self.added_doc)

        self.assertEqual(self.added_doc, Document(d_id=self.added_doc.d_id, desc="", request_id=None, grade=0))

    def test_2_read_request_success(self):
        self.assertEqual(dr.get_document(self.added_doc.d_id),
                         Document(d_id=self.added_doc.d_id, desc="", request_id=None, grade=0))

    def test_3_update_request_success(self):
        TestDocumentRepo.added_doc = dr.update_document(
            Document(d_id=self.added_doc.d_id, desc="new", request_id=None, grade=0))

        self.assertEqual(self.added_doc.desc, "new")

    def test_4_delete_request_success(self):
        self.assertIsNotNone(dr.delete_document(self.added_doc.d_id))


if __name__ == '__main__':
    unittest.main(failfast=True, exit=False)
