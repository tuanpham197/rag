import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv

# load_dotenv()

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "../../"))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CHROMA_DB_URL = os.getenv("CHROMA_DB_URL", "http://localhost:8001")
COLLECTION_NAME = "rag_collection"

def load_pdfs(data_dir: str) -> List[Document]:
    """Loads all PDFs from the specified directory."""
    documents = []
    if not os.path.exists(data_dir):
        print(f"Directory {data_dir} does not exist.")
        return []

    for filename in os.listdir(data_dir):
        if filename.endswith(".pdf"):
            filepath = os.path.join(data_dir, filename)
            print(f"Loading {filepath}...")
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            documents.extend(docs)
    return documents

import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def chunk_documents(documents: List['Document']) -> List['Document']:
    """
    Hàm này được mỗi tiến trình con gọi để xử lý một lô tài liệu.
    Lưu ý: text_splitter được khởi tạo bên trong hàm này để tránh các vấn đề
    về pickling (tuần tự hóa) đối tượng khi truyền qua các tiến trình.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=[
            "\n\n",      # Đoạn văn
            "\n",        # Dòng mới
            "●",         # Dấu đầu dòng (bullet point)
            "○",         # Dấu đầu dòng (bullet point)
            "\n- ",      # Dấu gạch đầu dòng
            "\. ",       # Dấu chấm theo sau là khoảng trắng
            " ",         # Từ
            ""           # Ký tự
        ],
        keep_separator=True,
    )
    return text_splitter.split_documents(documents)

# def chunk_documents_optimized(documents: List['Document'], num_processes: int = None) -> List['Document']:
#     """
#     Chunks tài liệu một cách hiệu quả bằng cách sử dụng xử lý đa tiến trình.
#     """
#     if not documents:
#         return []

#     start_time = time.time()

#     # Nếu không chỉ định số tiến trình, hãy sử dụng số lõi CPU có sẵn
#     if num_processes is None:
#         num_processes = multiprocessing.cpu_count()

#     # Đảm bảo không tạo nhiều tiến trình hơn số tài liệu
#     num_processes = min(num_processes, len(documents))

#     # Chia danh sách tài liệu thành các lô để phân phối cho các tiến trình
#     # Ví dụ: [1, 2, 3, 4, 5] với 2 tiến trình -> [[1, 2, 3], [4, 5]]
#     chunk_size = (len(documents) + num_processes - 1) // num_processes
#     doc_batches = [documents[i:i + chunk_size] for i in range(0, len(documents), chunk_size)]

#     with multiprocessing.Pool(processes=num_processes) as pool:
#         # Áp dụng hàm split_documents_batch cho mỗi lô tài liệu một cách song song
#         results = pool.map(split_documents_batch, doc_batches)

#     # Làm phẳng danh sách các chunks (vì results là một list của các list)
#     chunks = [chunk for sublist in results for chunk in sublist]

#     end_time = time.time()
#     duration = end_time - start_time
    
#     print(f"Split {len(documents)} documents into {len(chunks)} chunks in {duration:.4f} seconds using {num_processes} processes.")
    
#     return chunks

def index_documents(chunks: List[Document]):
    """Indexes chunks into ChromaDB."""
    if not chunks:
        print("No chunks to index.")
        return

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # Connect to ChromaDB (HttpClient mode)
    # Note: langchain-chroma might behave differently depending on version.
    # Using generic Chroma client setup.
    
    # If running strictly as client to a server:
    import chromadb
    client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST", "localhost"), port=int(os.getenv("CHROMA_PORT", "8001")))
    
    vector_store = Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )
    
    # Add documents
    # Chroma handles batching, but for large datasets we might want to batch manually.
    vector_store.add_documents(documents=chunks)
    print(f"Indexed {len(chunks)} chunks into ChromaDB collection '{COLLECTION_NAME}'.")

def delete_collection():
    """Deletes the ChromaDB collection."""
    import chromadb
    client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST", "localhost"), port=int(os.getenv("CHROMA_PORT", "8001")))
    try:
        client.delete_collection(COLLECTION_NAME)
        print(f"Deleted collection '{COLLECTION_NAME}'.")
    except Exception as e:
        print(f"Error deleting collection: {e}")

if __name__ == "__main__":
    print("Starting indexing pipeline...")
    docs = load_pdfs(DATA_DIR)
    chunks = chunk_documents(docs)
    index_documents(chunks)
    print("Indexing complete.")
