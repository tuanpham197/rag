import unittest
from unittest.mock import MagicMock, patch
from src.core.indexing import chunk_documents
from langchain_core.documents import Document
import os

class TestCore(unittest.TestCase):
    def test_chunk_documents(self):
        docs = [Document(page_content="a" * 2000, metadata={"source": "test.pdf", "page": 1})]
        chunks = chunk_documents(docs)
        self.assertTrue(len(chunks) > 1)
        self.assertEqual(chunks[0].metadata["source"], "test.pdf")
        self.assertEqual(chunks[0].metadata["page"], 1)

    @patch("src.core.querying.Chroma")
    @patch("src.core.querying.OpenAIEmbeddings")
    @patch("chromadb.HttpClient")
    def test_get_retriever(self, mock_http_client, mock_embeddings, mock_chroma):
        # Mock env vars to ensure we hit the code path
        with patch.dict(os.environ, {"CHROMA_HOST": "localhost", "CHROMA_PORT": "8001"}):
            from src.core.querying import get_retriever
            retriever = get_retriever()
            self.assertIsNotNone(retriever)

if __name__ == "__main__":
    unittest.main()
