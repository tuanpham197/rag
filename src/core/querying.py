import os
from typing import List, Dict, Any
from operator import itemgetter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

CHROMA_DB_URL = os.getenv("CHROMA_DB_URL", "http://localhost:8001")
COLLECTION_NAME = "rag_collection"

def get_vector_store():
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    import chromadb
    client = chromadb.HttpClient(host=os.getenv("CHROMA_HOST", "localhost"), port=int(os.getenv("CHROMA_PORT", "8001")))

    vector_store = Chroma(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )
    return vector_store

def get_retriever():
    vector_store = get_vector_store()
    return vector_store.as_retriever(search_kwargs={"k": 5})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_rag_chain():
    vector_store = get_vector_store()
    llm = ChatOllama(model="llama3")

    # System prompt for RAG
    from src.core.prompt.system_prompt import system_template
    
    # We need to handle chat history. 
    # For simplicity in this phase, we'll just use the question and context.
    # If chat_history is provided, it should be formatted into the prompt or used to contextualize the question.
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{question}"),
    ])

    def format_chat_history(history: List[Dict[str, str]]):
        messages = []
        if not history:
            return messages
        for msg in history:
            if msg.get("role") == "user":
                messages.append(HumanMessage(content=msg.get("content", "")))
            elif msg.get("role") == "assistant":
                messages.append(AIMessage(content=msg.get("content", "")))
        return messages

    # Helper to format history from the dict input
    def get_formatted_history(input_dict):
        return format_chat_history(input_dict.get("chat_history", []))

    # Use similarity_search directly via RunnableLambda
    from langchain_core.runnables import RunnableLambda
    
    def retrieve_docs(input_dict):
        question = input_dict["question"]
        print(question)
        return vector_store.similarity_search(question, k=5)

    chain = (
        RunnableParallel({
            "context": RunnableLambda(retrieve_docs),
            "question": itemgetter("question"),
            "chat_history": get_formatted_history,
        })
        .assign(answer= (
            RunnablePassthrough.assign(
                context=lambda x: format_docs(x["context"])
            )
            | prompt
            | llm
            | StrOutputParser()
        ))
    )

    return chain

async def query_rag(question: str, chat_history: List[Dict[str, str]] = None) -> Dict[str, Any]:
    chain = get_rag_chain()
    result = await chain.ainvoke({"question": question, "chat_history": chat_history})
    return result
