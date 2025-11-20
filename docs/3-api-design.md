# API Design for RAG Chatbox

This document outlines the API endpoints required to support the frontend chatbox application.

## Overview

The API is built using **FastAPI**. It provides endpoints for chatting with the RAG system, managing the document index, and checking system health.

## 1. Chat & Query Endpoints

### 1.1. Send Chat Message
**Endpoint**: `POST /api/chat`
**Description**: Sends a user message to the RAG system and receives a generated response with source citations.
**Use Case**: The main interaction for the chatbox.

**Request Body (JSON)**:
```json
{
  "question": "What are the safety protocols?",
  "session_id": "optional-session-uuid", 
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi! How can I help?"}
  ]
}
```
*Note: `history` is optional. If provided, the backend uses it for conversational context.*

**Response Body (JSON)**:
```json
{
  "answer": "The safety protocols include...",
  "sources": [
    {
      "filename": "safety_manual.pdf",
      "page": 12,
      "snippet": "...wear safety goggles..."
    }
  ],
  "processing_time": 0.45
}
```

### 1.2. Stream Chat Message (Optional but Recommended)
**Endpoint**: `POST /api/chat/stream`
**Description**: Same as `/api/chat` but returns a Server-Sent Events (SSE) stream for a typewriter effect.

## 2. Document Management (Indexing)

### 2.1. Trigger Indexing
**Endpoint**: `POST /api/index`
**Description**: Triggers the background process to read PDF files from the `document/` folder and update the vector database.
**Use Case**: Admin or "Refresh Knowledge Base" button.

**Response Body (JSON)**:
```json
{
  "status": "success",
  "message": "Indexing started",
  "documents_found": 5
}
```

### 2.2. List Indexed Documents
**Endpoint**: `GET /api/documents`
**Description**: Returns a list of documents currently available in the knowledge base.
**Use Case**: To show the user what information the bot has access to.

**Response Body (JSON)**:
```json
{
  "documents": [
    {"filename": "policy.pdf", "indexed_at": "2023-10-27T10:00:00Z"},
    {"filename": "report.pdf", "indexed_at": "2023-10-27T10:05:00Z"}
  ]
}
```

## 3. Feedback & Evaluation

### 3.1. Submit Feedback
**Endpoint**: `POST /api/feedback`
**Description**: Allows users to rate an answer (thumbs up/down).
**Use Case**: Collecting ground truth data for Ragas evaluation.

**Request Body (JSON)**:
```json
{
  "question": "...",
  "answer": "...",
  "rating": 1, // 1 for upvote, -1 for downvote
  "comment": "Very helpful"
}
```

## 4. System

### 4.1. Health Check
**Endpoint**: `GET /health`
**Description**: Returns the status of the API and Database connection.
**Use Case**: Load balancers and frontend readiness check.

**Response Body (JSON)**:
```json
{
  "status": "ok",
  "version": "1.0.0"
}
```

