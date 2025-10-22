import requests
import json

def test_ml_service():
    print("🧪 Testing ML service directly...")
    
    try:
        # Test health endpoint
        health_response = requests.get('http://localhost:5000/health', timeout=5)
        print(f"Health check: {health_response.status_code}")
        print(f"Health data: {health_response.json()}")
        
        # Test chat with necklace query
        chat_data = {"message": "I want to check necklaces"}
        chat_response = requests.post(
            'http://localhost:5000/chat', 
            json=chat_data,
            timeout=5
        )
        print(f"\nChat response status: {chat_response.status_code}")
        print(f"Chat response: {json.dumps(chat_response.json(), indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_ml_service()