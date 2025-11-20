
# Project: RAG Application (Python, LangChain, OpenAI, FastAPI)

## 1. Project Overview
This project is a Retrieval-Augmented Generation (RAG) system built with Python, LangChain, and OpenAI.
It processes PDF documents, indexes them into a Vector Database (ChromaDB), and allows users to query the information via an LLM.
It exposes a REST API using **FastAPI** and includes an evaluation pipeline using **Ragas**.

## 2. Directory Structure
- `data/`: Stores input PDF files for indexing (formerly document/).
- `chromadb/`: Directory for ChromaDB Docker configuration or persistent storage.
- `src/`: Source code.
    - `api/`: FastAPI routers and application entry point.
    - `core/`: Core RAG logic (indexing, querying, embedding).
    - `models/`: Pydantic data models.
- `tests/`: Unit and integration tests.
- `docs/`: Documentation.
- `evaluation/`: Ragas evaluation scripts and datasets.
- `.env`: Environment variables (not committed).

## 3. Tech Stack
- **Language**: Python 3.10+
- **Package Manager**: uv
- **API Framework**: FastAPI, Uvicorn
- **Orchestration**: LangChain
- **LLM**: OpenAI (GPT-4o-mini or similar)
- **Vector Database**: ChromaDB (Dockerized)
- **PDF Parsing**: pypdf (via LangChain PyPDFLoader)
- **Chunking**: RecursiveCharacterTextSplitter
- **Evaluation**: Ragas
- **Env Management**: python-dotenv

## 4. Workflow Implementation Details

### Phase 1: Indexing Pipeline
1.  **Load Data**:
    - Use `PyPDFLoader` to load PDFs from `data/`.
2.  **Metadata Preservation**:
    - **Critical**: Ensure every document object retains `source` (filename) and `page` metadata.
3.  **Chunking**:
    - Use `RecursiveCharacterTextSplitter`.
    - Default: `chunk_size=1000`, `chunk_overlap=200`.
4.  **Embedding & Storage**:
    - Embed chunks using `OpenAIEmbeddings`.
    - Persist to ChromaDB collection.

### Phase 2: Querying Pipeline
1.  **Input Handling**: Accept `question` and optional `chat_history`.
2.  **Vector Search**:
    - Retrieve `k=4` most relevant chunks.
    - **Outcome**: Must return text content AND metadata (citations).
3.  **Augmentation**:
    - Construct a prompt using System Message (Context) + Human Message (Question).
4.  **Generation**:
    - Stream the response from OpenAI.

### Phase 3: Evaluation Pipeline (Ragas)
1.  **Dataset**: Create a "Golden Dataset" with `question` and `ground_truth`.
2.  **Metrics**: Faithfulness, Answer Relevancy, Context Precision, Context Recall.
3.  **Output**: Export results to CSV for analysis.

### Phase 4: API Layer (FastAPI)
1.  **Endpoints**:
    - `POST /api/chat`: Input `{question, history}` -> Output `{answer, sources}`.
    - `POST /api/index`: Triggers indexing (Use `BackgroundTasks` to avoid blocking).
    - `GET /health`: Returns status 200.
2.  **Async**: All DB and LLM interactions must be `async`.

## 5. Setup Instructions

### Prerequisites
- Python 3.x, uv, Docker.

### Installation
1.  Install dependencies:
    ```bash
    uv venv
    source .venv/bin/activate
    uv pip install langchain langchain-openai langchain-community chromadb pypdf python-dotenv ragas pandas fastapi uvicorn python-multipart httpx
    ```

### Database Setup (ChromaDB)
- Run ChromaDB on **Port 8001** to avoid conflict with FastAPI (8000).
    ```bash
    docker run -p 8001:8000 chromadb/chroma
    ```
- In `.env`, set `CHROMA_HOST=localhost` and `CHROMA_PORT=8001`.

### Configuration
- `.env` content:
    ```
    OPENAI_API_KEY=sk-...
    CHROMA_DB_URL=http://localhost:8001
    ```

## 6. Coding Rules
- **Type Hinting**: Use strict Python type hinting (e.g., `def func(x: str) -> list[str]:`).
- **Async/Await**: Use `await` for all I/O bound operations (OpenAI calls, DB lookups).
- **Error Handling**: Use `try/except` blocks specifically around external API calls.
- **Metadata**: Never drop metadata during the pipeline; the frontend needs it for citations.
- **Pydantic**: Use Pydantic models for all API Inputs/Outputs.