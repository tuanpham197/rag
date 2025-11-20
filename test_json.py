from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class TestModel(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline of the joke")

def test_json_output():
    print("Testing JSON output capability of llama3...")
    llm = ChatOllama(model="llama3", temperature=0, format="json")
    
    parser = JsonOutputParser(pydantic_object=TestModel)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant. Output only valid JSON."),
        ("human", "Tell me a joke about Python.\n{format_instructions}")
    ])
    
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({"format_instructions": parser.get_format_instructions()})
        print("Success! JSON Output:")
        print(result)
    except Exception as e:
        print(f"Failed to generate JSON: {e}")

if __name__ == "__main__":
    test_json_output()
