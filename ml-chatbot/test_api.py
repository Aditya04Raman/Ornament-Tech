import requests
import json

def test_chatbot_api():
    """
    Test the ML chatbot API endpoints
    """
    base_url = "http://localhost:5000"
    
    print("Testing ML Chatbot API...")
    print("=" * 50)
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        print()
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test chat endpoint
    test_questions = [
        "What is Ornament Tech?",
        "How much do engagement rings cost?",
        "Tell me about the bespoke process",
        "What materials do you use?",
        "How can I book a consultation?",
        "Do you offer repairs?",
        "Thank you"
    ]
    
    print("Testing Chat Responses:")
    print("-" * 30)
    
    for question in test_questions:
        try:
            response = requests.post(
                f"{base_url}/chat",
                headers={"Content-Type": "application/json"},
                json={"message": question}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"Q: {question}")
                print(f"A: {data['response']}")
                print(f"Intent: {data['intent']} (confidence: {data['confidence']})")
                print(f"Response Type: {data['response_type']}")
                print("-" * 50)
            else:
                print(f"Error for '{question}': {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"Failed to test '{question}': {e}")
    
    # Test model info
    try:
        response = requests.get(f"{base_url}/model-info")
        print("Model Information:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Model info failed: {e}")

if __name__ == "__main__":
    test_chatbot_api()
