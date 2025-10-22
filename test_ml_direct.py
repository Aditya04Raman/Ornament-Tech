#!/usr/bin/env python3
"""
Direct test of ML chatbot functionality
"""
import sys
import os

# Add the ml-chatbot directory to path
ml_chatbot_path = os.path.join(os.path.dirname(__file__), 'ml-chatbot')
sys.path.append(ml_chatbot_path)

# Import our lightweight chatbot
from lightweight_ml_service import LightweightJewelryChatbot

def test_ml_chatbot():
    print("🧪 Testing ML Chatbot Directly...")
    
    # Create chatbot instance
    chatbot = LightweightJewelryChatbot()
    
    # Load models
    if chatbot.load_models():
        print("✅ Models loaded successfully!")
    else:
        print("⚠️ Running with basic capabilities")
    
    # Test different types of messages
    test_messages = [
        "Hello there!",
        "I want to book an appointment",
        "Show me diamond engagement rings",
        "What materials do you use?",
        "How much does a wedding ring cost?",
        "Tell me about your bespoke process"
    ]
    
    print("\n🔄 Testing ML Responses:")
    print("=" * 50)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. User: {message}")
        
        try:
            response = chatbot.generate_response(message)
            print(f"   Bot: {response['response'][:100]}...")
            print(f"   Method: {response['method']}")
            print(f"   Intent: {response['intent']}")
            print(f"   Confidence: {response['confidence']}")
        except Exception as e:
            print(f"   ERROR: {e}")
    
    print("\n✅ ML Chatbot test completed!")

if __name__ == "__main__":
    test_ml_chatbot()