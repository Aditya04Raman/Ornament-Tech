"""
Test script to verify ML chatbot integration is working
"""

import requests
import json

def test_ml_service():
    print("🧪 Testing ML Chatbot Service...")
    
    # Test health endpoint
    try:
        health_response = requests.get("http://localhost:5000/health")
        if health_response.status_code == 200:
            health_data = health_response.json()
            print(f"✅ Health Check: {health_data}")
        else:
            print(f"❌ Health check failed: {health_response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to ML service: {e}")
        return
    
    # Test chat functionality
    test_messages = [
        "Hello, I'm interested in engagement rings",
        "What diamond shapes do you recommend?",
        "Can you tell me about pricing?",
        "I'd like to book an appointment",
        "Thank you for your help"
    ]
    
    print("\n💬 Testing Chat Responses:")
    print("=" * 50)
    
    for message in test_messages:
        try:
            response = requests.post(
                "http://localhost:5000/chat",
                json={"message": message},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"\n👤 User: {message}")
                print(f"🤖 Bot: {data['response'][:200]}...")
                print(f"📊 Method: {data['method']}, Intent: {data['intent']}, Confidence: {data['confidence']:.2f}")
            else:
                print(f"❌ Chat failed for '{message}': {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error testing '{message}': {e}")
    
    print("\n✅ ML Service Testing Complete!")

if __name__ == "__main__":
    test_ml_service()