# RAG API Documentation

## Introduction
This API provides endpoints for a Retrieval-Augmented Generation (RAG) system. It allows users to query a knowledge base and trigger background indexing of documents.

## Base URL
The API is served at `http://localhost:8000` (default).

## Endpoints

### 1. Health Check
Checks if the API is running.

- **URL**: `/health`
- **Method**: `GET`
- **Response**: JSON object indicating status.

**Example Response:**
```json
{
  "status": "ok"
}
```

### 2. Trigger Indexing
Triggers the background indexing process for documents in the data directory.

- **URL**: `/api/index`
- **Method**: `POST`
- **Response**: JSON object confirming the task has been started.

**Example Response:**
```json
{
  "message": "Indexing triggered in background."
}
```

### 3. Chat
Submit a question to the RAG system and receive an answer with sources.

- **URL**: `/api/chat`
- **Method**: `POST`
- **Request Body**: JSON object containing the question and optional chat history.

**Request Model (`QueryRequest`):**
| Field | Type | Description | Required |
|---|---|---|---|
| `question` | `string` | The user's question. | Yes |
| `chat_history` | `array` | List of previous message dictionaries. | No |

**Example Request:**
```json
{
  "question": "What is the capital of France?",
  "chat_history": []
}
```

**Example cURL Request:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "question": "What is the capital of France?",
           "chat_history": []
         }'
```

- **Response**: JSON object containing the generated answer and source documents.

**Response Model (`QueryResponse`):**
| Field | Type | Description |
|---|---|---|
| `answer` | `string` | The generated answer from the LLM. |
| `sources` | `array` | List of source documents used for the answer. |

**Source Model (`DocumentSource`):**
| Field | Type | Description |
|---|---|---|
| `source` | `string` | The filename or source of the document. |
| `page` | `integer` | The page number (if applicable). |
| `content` | `string` | The content snippet used. |

**Example Response:**
```json
{
  "answer": "The capital of France is Paris.",
  "sources": [
    {
      "source": "geography_book.pdf",
      "page": 12,
      "content": "Paris is the capital and most populous city of France."
    }
  ]
}
```
