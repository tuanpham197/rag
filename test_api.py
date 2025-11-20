import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    print("Testing /health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Is it running?")

def test_chat():
    print("\nTesting /api/chat...")
    payload = {
        "question": "What is the tech stack?",
        "chat_history": []
    }
    try:
        response = requests.post(f"{BASE_URL}/api/chat", json=payload)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("Answer:", data["answer"])
            print("Sources:", [s["source"] for s in data["sources"]])
        else:
            print("Error:", response.text)
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API. Is it running?")

if __name__ == "__main__":
    test_health()
    test_chat()
