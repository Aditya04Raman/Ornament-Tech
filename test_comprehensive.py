import requests
import json

def test_comprehensive_chatbot():
    print("🧪 Testing Comprehensive ML Chatbot...")
    
    test_queries = [
        "I want to check necklaces",
        "Show me engagement rings", 
        "Tell me about your craftsmanship",
        "How do I book an appointment?",
        "What are your store locations?",
        "I need help with ring sizing",
        "Tell me about your collections",
        "What gemstones do you offer?",
        "How much do wedding bands cost?",
        "Show me your galleries"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Testing: '{query}'")
        
        try:
            response = requests.post(
                'http://localhost:5000/chat',
                json={"message": query},
                timeout=5
            )
            
            if response.ok:
                data = response.json()
                print(f"   ✅ Intent: {data['intent']}")
                print(f"   📊 Confidence: {data['confidence']}")
                print(f"   🔧 Method: {data['method']}")
                print(f"   💬 Response: {data['response'][:100]}...")
            else:
                print(f"   ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print("\n✅ Comprehensive chatbot test completed!")

if __name__ == "__main__":
    test_comprehensive_chatbot()