from pydantic import BaseModel, Field
from typing import List, Optional

class DocumentSource(BaseModel):
    source: str
    page: int
    content: str

class QueryRequest(BaseModel):
    question: str
    chat_history: Optional[List[dict]] = None # List of message dicts or strings

class QueryResponse(BaseModel):
    answer: str
    sources: List[DocumentSource]
