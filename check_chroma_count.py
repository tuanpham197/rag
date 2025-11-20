import os
import chromadb
from dotenv import load_dotenv

load_dotenv()

CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8001"))
COLLECTION_NAME = "rag_collection"

def check_count():
    try:
        print(f"Connecting to ChromaDB at {CHROMA_HOST}:{CHROMA_PORT}...")
        client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
        
        try:
            collection = client.get_collection(COLLECTION_NAME)
            count = collection.count()
            print(f"Successfully connected to collection '{COLLECTION_NAME}'.")
            print(f"Total documents in collection: {count}")
            
            if count > 0:
                print("chunk_documents run likely SUCCESSFUL (documents found).")
                # Optionally peek at one
                print("Sample document metadata:", collection.peek(limit=1)['metadatas'])
            else:
                print("chunk_documents run likely FAILED or NOT RUN (0 documents found).")
                
        except ValueError:
             print(f"Collection '{COLLECTION_NAME}' does not exist. chunk_documents definitely has not run or failed completely.")

    except Exception as e:
        print(f"Error connecting to ChromaDB: {e}")

if __name__ == "__main__":
    check_count()
