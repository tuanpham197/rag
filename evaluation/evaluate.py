import os
import sys
import asyncio
import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall,
)
from dotenv import load_dotenv

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.core.querying import query_rag

load_dotenv()

# Sample dataset - In a real scenario, load this from a file
SAMPLE_DATASET = [
    {
        "question": "What is the tech stack of this project?",
        "ground_truth": "The tech stack includes Python, LangChain, OpenAI, ChromaDB, FastAPI, and Ragas."
    }
]

async def run_evaluation():
    print("Starting evaluation...")
    
    questions = [item["question"] for item in SAMPLE_DATASET]
    ground_truths = [item["ground_truth"] for item in SAMPLE_DATASET]
    
    answers = []
    contexts = []
    
    for question in questions:
        print(f"Processing question: {question}")
        try:
            result = await query_rag(question)
            answers.append(result["answer"])
            # Ragas expects list of strings for contexts
            contexts.append([doc.page_content for doc in result["context"]])
        except Exception as e:
            print(f"Error processing question '{question}': {e}")
            answers.append("Error")
            contexts.append([])
        
    data = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    
    dataset = Dataset.from_dict(data)
    
    # Check for OpenAI API Key
    # if not os.getenv("OPENAI_API_KEY"):
    #     print("Error: OPENAI_API_KEY not found in environment variables.")
    #     print("Please set it in .env file.")
    #     return

    from langchain_ollama import ChatOllama, OllamaEmbeddings
    
    # Explicitly define LLM and Embeddings for Ragas
    # Use temperature=0 for deterministic output
    # format="json" forces the model to output valid JSON, which helps with Ragas parsing
    llm = ChatOllama(model="llama3", temperature=0)
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    from ragas.run_config import RunConfig

    # Configure run settings for local LLM
    # Reduce workers to 1 to avoid overloading Ollama
    # Increase timeout to handle slower local inference
    # Add retries to handle transient failures
    run_config = RunConfig(
        max_workers=1,
        timeout=600,
        max_retries=3,
    )

    # Note: Ragas requires OpenAI API key to be set in environment
    try:
        results = evaluate(
            dataset=dataset,
            metrics=[
                faithfulness,
                answer_relevancy,
                context_precision,
                context_recall,
            ],
            llm=llm,
            embeddings=embeddings,
            run_config=run_config,
            raise_exceptions=False,
        )
        
        print("Evaluation Results:")
        print(results)
        
        df = results.to_pandas()
        output_path = "evaluation/results.csv"
        df.to_csv(output_path, index=False)
        print(f"Results saved to {output_path}")
    except Exception as e:
        print(f"An error occurred during evaluation: {e}")


if __name__ == "__main__":
    asyncio.run(run_evaluation())
