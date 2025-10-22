"""Quick test to verify ML chatbot is working"""
import requests
import time

print("=" * 60)
print("QUICK ML CHATBOT TEST")
print("=" * 60)

# Wait a moment for server to be ready
time.sleep(2)

# Test health endpoint
try:
    health_response = requests.get("http://localhost:5000/health", timeout=5)
    if health_response.status_code == 200:
        data = health_response.json()
        print(f"\n✅ ML Chatbot is running!")
        print(f"   Jewelry items: {data.get('jewelry_items', 0)}")
        print(f"   Diamonds: {data.get('diamonds', 0)}")
    else:
        print(f"\n❌ Health check failed with status {health_response.status_code}")
        exit(1)
except Exception as e:
    print(f"\n❌ Cannot connect to ML chatbot: {e}")
    print("   Please start it with: START_ML_CHATBOT.bat")
    exit(1)

# Test 5 critical questions
test_questions = [
    "What types of jewellery do you have?",
    "Show me diamond rings under $3000",
    "Tell me about diamond quality",
    "Gold engagement ring, custom, under $5000, ship?",
    "How do I clean my jewelry?"
]

print("\n" + "=" * 60)
print("TESTING 5 CRITICAL QUESTIONS")
print("=" * 60)

all_passed = True

for i, question in enumerate(test_questions, 1):
    try:
        response = requests.post(
            "http://localhost:5000/chat",
            json={"message": question},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('response', '')
            intent = data.get('intent', 'unknown')
            
            # Check if it's a generic response
            generic_indicators = [
                "Welcome to Ornament Tech",
                "I don't understand",
                "Could you rephrase",
                "I'm not sure"
            ]
            
            is_generic = any(indicator.lower() in answer.lower() for indicator in generic_indicators)
            has_substance = len(answer) > 100  # Specific answers should be detailed
            
            if is_generic or not has_substance:
                print(f"\n❌ Question {i} FAILED")
                print(f"   Q: {question}")
                print(f"   Intent: {intent}")
                print(f"   Response too generic or short:")
                print(f"   {answer[:200]}...")
                all_passed = False
            else:
                print(f"\n✅ Question {i} PASSED")
                print(f"   Q: {question}")
                print(f"   Intent: {intent}")
                print(f"   Response length: {len(answer)} chars")
                print(f"   Preview: {answer[:150]}...")
        else:
            print(f"\n❌ Question {i} ERROR")
            print(f"   Q: {question}")
            print(f"   HTTP Status: {response.status_code}")
            all_passed = False
            
    except Exception as e:
        print(f"\n❌ Question {i} EXCEPTION")
        print(f"   Q: {question}")
        print(f"   Error: {e}")
        all_passed = False

# Final result
print("\n" + "=" * 60)
if all_passed:
    print("🎉 ALL TESTS PASSED!")
    print("✅ ML Chatbot is working properly")
    print("✅ No generic responses detected")
    print("✅ Ready for presentation!")
else:
    print("❌ SOME TESTS FAILED")
    print("Please check the responses above")
print("=" * 60)
