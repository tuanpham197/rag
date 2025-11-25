import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from contextlib import asynccontextmanager
from src.models.models import QueryRequest, QueryResponse, DocumentSource
from src.core.querying import query_rag
from src.core.indexing import load_pdfs, chunk_documents, index_documents, DATA_DIR
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic if needed
    yield
    # Shutdown logic if needed

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="RAG API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

def run_indexing():
    print("Running background indexing...")
    docs = load_pdfs(DATA_DIR)
    chunks = chunk_documents(docs)
    index_documents(chunks)
    print("Background indexing complete.")

@app.post("/api/index")
async def trigger_indexing(background_tasks: BackgroundTasks):
    background_tasks.add_task(run_indexing)
    return {"message": "Indexing triggered in background."}

@app.post("/api/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    try:
        # Convert pydantic models to dicts for the chain if needed, or just pass list of dicts
        history = request.chat_history if request.chat_history else []
        
        result = await query_rag(request.question, history)
        
        answer = result["answer"]
        source_docs = result["context"]
        
        sources = []
        for doc in source_docs:
            sources.append(DocumentSource(
                source=doc.metadata.get("source", "unknown"),
                page=doc.metadata.get("page", 0),
                content=doc.page_content
            ))
            
        return QueryResponse(answer=answer, sources=sources)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=8000, reload=True)
