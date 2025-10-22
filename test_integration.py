"""
Quick test to verify ML chatbot + website integration
"""

import requests
import time

def test_ml_chatbot():
    """Test ML chatbot is running"""
    print("\n" + "="*60)
    print("🔧 TESTING ML CHATBOT")
    print("="*60)
    
    try:
        # Test health endpoint
        health = requests.get("http://localhost:5000/health", timeout=2)
        if health.status_code == 200:
            data = health.json()
            print(f"✅ ML Chatbot is RUNNING")
            print(f"   📊 Jewelry items: {data.get('jewelry_items', 0):,}")
            print(f"   💎 Diamonds: {data.get('diamonds', 0):,}")
            return True
        else:
            print(f"❌ ML Chatbot returned status {health.status_code}")
            return False
    except Exception as e:
        print(f"❌ ML Chatbot NOT running")
        print(f"   Error: {e}")
        print(f"   → Start it with: START_ML_CHATBOT.bat")
        return False

def _probe(url: str, timeout=2):
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code == 200
    except Exception:
        return False

def test_website():
    """Test website is running (auto-detect 3001 or 3002)"""
    print("\n" + "="*60)
    print("🌐 TESTING WEBSITE")
    print("="*60)

    urls = ["http://localhost:3001", "http://localhost:3002"]
    active_url = None
    for url in urls:
        if _probe(url):
            active_url = url
            break

    if active_url:
        print(f"✅ Website is RUNNING on {active_url}")
        globals()["ACTIVE_SITE_URL"] = active_url
        return True

    print(f"❌ Website NOT running on 3001 or 3002")
    print(f"   → Start it with: START_WEBSITE.bat")
    return False

def test_website_ml_integration():
    """Test that website can talk to ML chatbot"""
    print("\n" + "="*60)
    print("🔗 TESTING WEBSITE → ML CHATBOT INTEGRATION")
    print("="*60)
    base = globals().get("ACTIVE_SITE_URL", "http://localhost:3001")
    try:
        # Send a question through the website's chat API
        test_question = "what types of jewellery do you have?"
        
        print(f"📤 Sending: '{test_question}'")
        print(f"   to {base}/api/chat")
        
        response = requests.post(
            f"{base}/api/chat",
            json={"message": test_question},
            timeout=10
        )
        
        if response.status_code == 200:
            # Parse SSE response
            content = response.text
            
            # Check if response contains data-driven content
            has_data = any(keyword in content.lower() for keyword in [
                'categories', 'materials', 'gemstones', 'pieces', 
                'jewelry categories', 'premium materials'
            ])
            
            if has_data:
                print(f"✅ Integration WORKING!")
                print(f"   Response contains dataset information")
                print(f"   Preview: {content[:200]}...")
                return True
            else:
                print(f"⚠️  Integration PARTIAL")
                print(f"   Website responded but content seems generic")
                print(f"   Preview: {content[:200]}...")
                return False
        else:
            print(f"❌ Website chat API returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Integration test FAILED")
        print(f"   Error: {e}")
        return False

def test_ml_direct():
    """Test ML chatbot directly"""
    print("\n" + "="*60)
    print("🤖 TESTING ML CHATBOT DIRECTLY")
    print("="*60)
    
    try:
        test_question = "what types of jewellery do you have?"
        print(f"📤 Asking ML chatbot: '{test_question}'")
        
        response = requests.post(
            "http://localhost:5000/chat",
            json={"message": test_question},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get('response', '')
            intent = data.get('intent', 'unknown')
            
            print(f"✅ ML Chatbot responded")
            print(f"   Intent detected: {intent}")
            print(f"   Response length: {len(answer)} chars")
            print(f"   Preview: {answer[:200]}...")
            return True
        else:
            print(f"❌ ML Chatbot returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ ML Chatbot direct test FAILED")
        print(f"   Error: {e}")
        return False

def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║         INTEGRATION VERIFICATION TEST                    ║
║                                                          ║
║  This script tests:                                      ║
║  1. ML Chatbot server (port 5000)                       ║
║  2. Website server (port 3001)                          ║
║  3. Integration between them                            ║
║  4. ML chatbot direct responses                         ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    results = {
        "ML Chatbot Running": test_ml_chatbot(),
        "Website Running": test_website(),
    }
    
    # Only test integration if both are running
    if results["ML Chatbot Running"]:
        results["ML Direct Response"] = test_ml_direct()
    else:
        results["ML Direct Response"] = False
        print("\n⚠️  Skipping ML direct test (chatbot not running)")
    
    if results["ML Chatbot Running"] and results["Website Running"]:
        results["Website→ML Integration"] = test_website_ml_integration()
    else:
        results["Website→ML Integration"] = False
        print("\n⚠️  Skipping integration test (services not running)")
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(results.values())
    total_count = len(results)
    
    print("\n" + "="*60)
    print(f"Results: {passed_count}/{total_count} tests passed")
    print("="*60)
    
    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Your ML chatbot is fully integrated with the website!")
        print("✅ Ready for presentation!")
        print("\n📍 Open http://localhost:3001 and click the chat widget to test!")
    elif results["ML Chatbot Running"] and results["Website Running"]:
        print("\n⚠️  Services are running but integration needs checking")
        print("   Try asking questions in the chat widget at http://localhost:3001")
    else:
        print("\n❌ Some services are not running")
        print("\n📝 To fix:")
        if not results["ML Chatbot Running"]:
            print("   1. Run: START_ML_CHATBOT.bat")
        if not results["Website Running"]:
            print("   2. Run: START_WEBSITE.bat")
        print("   OR just run: START_EVERYTHING.bat")

if __name__ == "__main__":
    main()
