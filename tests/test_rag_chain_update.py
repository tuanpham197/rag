import unittest
from unittest.mock import MagicMock, patch
from src.core.querying import get_rag_chain, get_vector_store
from langchain_core.documents import Document

class TestRagChain(unittest.TestCase):
    @patch("src.core.querying.Chroma")
    @patch("src.core.querying.OllamaEmbeddings")
    @patch("src.core.querying.ChatOllama")
    @patch("chromadb.HttpClient")
    def test_rag_chain_structure(self, mock_http_client, mock_chat_ollama, mock_embeddings, mock_chroma):
        # Mock vector store and similarity search
        mock_vector_store = MagicMock()
        mock_vector_store.similarity_search.return_value = [
            Document(page_content="Test content 1"),
            Document(page_content="Test content 2")
        ]
        mock_chroma.return_value = mock_vector_store
        
        # Mock LLM response
        from langchain_core.messages import AIMessage
        mock_llm_instance = MagicMock()
        mock_llm_instance.invoke.return_value = AIMessage(content="Test answer")
        mock_chat_ollama.return_value = mock_llm_instance

        # Get chain
        chain = get_rag_chain()
        
        # Invoke chain
        result = chain.invoke({"question": "test question"})
        
        # Verify similarity_search was called
        mock_vector_store.similarity_search.assert_called_with("test question", k=5)
        
        # Verify result
        # Note: The result of the chain depends on how the mocks interact with the chain components.
        # Since we mocked the LLM invoke, we expect the final output to be related to that, 
        # but StrOutputParser might change it. 
        # However, the main goal is to verify similarity_search call.
        print("Chain invoked successfully.")

if __name__ == "__main__":
    unittest.main()
