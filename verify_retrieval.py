import asyncio
from src.core.querying import query_rag

async def test_retrieval():
    question = "What is the tech stack of this project?"
    print(f"Question: {question}")
    result = await query_rag(question)
    print("\nAnswer:")
    print(result["answer"])
    print("\nSources:")
    for doc in result["context"]:
        print(f"- {doc.metadata.get('source', 'Unknown')}")

if __name__ == "__main__":
    asyncio.run(test_retrieval())
