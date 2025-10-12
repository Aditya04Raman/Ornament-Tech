import requests
import json
import time

def test_conversation():
    """
    Test the chatbot with sample conversations
    """
    base_url = "http://localhost:5000"
    
    print("🤖 Testing Ornament Tech ML Chatbot")
    print("=" * 50)
    
    # Test if server is running
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Chatbot API is running!")
            health_data = response.json()
            print(f"Status: {health_data['status']}")
            print(f"Service: {health_data['service']}")
            print(f"Chatbot Ready: {health_data['chatbot_ready']}")
        else:
            print("❌ API not responding properly")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to chatbot API: {e}")
        print("Make sure the Flask server is running on http://localhost:5000")
        return False
    
    print("\n💬 Starting Conversation Tests...")
    print("-" * 50)
    
    # Sample conversation
    questions = [
        "Hello!",
        "What is Ornament Tech?",
        "How much do engagement rings cost?",
        "Tell me about your bespoke process",
        "What materials do you work with?",
        "Can I book a consultation?",
        "Do you offer repairs?",
        "Thank you!"
    ]
    
    for i, question in enumerate(questions, 1):
        try:
            print(f"\n{i}. 👤 You: {question}")
            
            response = requests.post(
                f"{base_url}/chat",
                headers={"Content-Type": "application/json"},
                json={"message": question},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"🤖 Bot: {data['response']}")
                print(f"   📊 Intent: {data['intent']} (confidence: {data['confidence']:.2f})")
                print(f"   🔍 Type: {data['response_type']}")
                
                time.sleep(1)  # Brief pause between messages
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Conversation test completed!")
    return True

if __name__ == "__main__":
    test_conversation()
