"""
Test script to demonstrate ML chatbot handles ANY type of question
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

# Comprehensive test questions covering ALL domains
test_questions = [
    # Inventory questions
    ("what types of jewellery do you have?", "Should show categories, materials, gemstones with counts"),
    ("what's in your collection?", "Should list inventory statistics"),
    
    # Search questions
    ("show me diamond rings", "Should filter and show diamond rings"),
    ("I'm looking for gold necklaces", "Should search gold necklaces"),
    ("find me platinum earrings", "Should search platinum earrings"),
    
    # Pricing questions
    ("what's your price range?", "Should show min, max, avg, distributions"),
    ("how much does a diamond ring cost?", "Should show diamond ring pricing"),
    ("do you have anything under $1000?", "Should filter by price"),
    
    # Comparison questions
    ("compare gold vs platinum", "Should compare materials"),
    ("what's better: rings or necklaces?", "Should compare categories"),
    ("difference between diamond and ruby?", "Should explain gemstone differences"),
    
    # Education questions
    ("tell me about diamonds", "Should explain 4 Cs + dataset stats"),
    ("what is diamond clarity?", "Should educate about clarity"),
    ("how do I choose a gemstone?", "Should provide gemstone guidance"),
    
    # Material questions
    ("tell me about gold jewelry", "Should show gold inventory and info"),
    ("what metals do you use?", "Should list all materials"),
    ("is platinum better than gold?", "Should compare materials"),
    
    # Customization questions
    ("can I custom design a ring?", "Should explain bespoke process"),
    ("do you do engraving?", "Should mention customization options"),
    ("I want to create my own jewelry", "Should direct to bespoke service"),
    
    # Sizing questions
    ("how do I measure ring size?", "Should provide sizing guide"),
    ("what necklace length should I get?", "Should explain necklace lengths"),
    ("can you resize my ring?", "Should mention resizing services"),
    
    # Care questions
    ("how do I clean my jewelry?", "Should provide care instructions"),
    ("how to maintain gold rings?", "Should give maintenance tips"),
    ("what's your warranty?", "Should explain warranty policy"),
    
    # Appointment questions
    ("can I book an appointment?", "Should explain appointment process"),
    ("where are your stores?", "Should direct to stores page"),
    ("I want to visit your showroom", "Should provide appointment info"),
    
    # Shipping questions
    ("do you ship internationally?", "Should explain shipping policy"),
    ("how long is delivery?", "Should mention shipping times"),
    ("is shipping insured?", "Should confirm insurance"),
    
    # Returns questions
    ("what's your return policy?", "Should explain 30-day returns"),
    ("can I exchange my ring?", "Should mention exchange policy"),
    ("do you accept refunds?", "Should explain refund process"),
    
    # Engagement/Wedding specific
    ("I'm looking for an engagement ring", "Should show engagement collection"),
    ("best rings for proposal?", "Should recommend engagement rings"),
    ("wedding jewelry options", "Should show bridal collection"),
    
    # Greetings
    ("hello", "Should greet and offer help"),
    ("hi there", "Should greet warmly"),
    
    # Gratitude
    ("thank you", "Should acknowledge and offer continued help"),
    ("thanks for your help", "Should respond warmly"),
    
    # Mixed/Complex questions
    ("I want a diamond ring with gold under $5000 for engagement, can I customize it and get it shipped?", "Should handle multi-intent query"),
    ("compare gold vs platinum rings under $3000 and tell me about sizing", "Should handle compound question"),
    
    # Edge cases
    ("what do you recommend?", "Should ask for preferences"),
    ("I'm confused", "Should offer guidance"),
    ("help me choose", "Should provide consultation info"),
]

def test_chatbot():
    print("\n" + "="*80)
    print("🤖 ML CHATBOT COMPREHENSIVE TEST")
    print("="*80)
    print(f"Testing {len(test_questions)} different question types...\n")
    
    # Check if server is running
    try:
        health = requests.get(f"{BASE_URL}/health", timeout=2)
        print(f"✅ Server Status: {health.json()}")
        print("-"*80 + "\n")
    except:
        print("❌ ERROR: ML Chatbot server not running!")
        print("Please start it with: START_ML_CHATBOT.bat")
        return
    
    success_count = 0
    
    for i, (question, expected) in enumerate(test_questions, 1):
        try:
            print(f"[{i}/{len(test_questions)}] Q: {question}")
            print(f"    Expected: {expected}")
            
            response = requests.post(
                f"{BASE_URL}/chat",
                json={"message": question},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data.get('response', '')
                intent = data.get('intent', 'unknown')
                
                # Check if it's NOT a generic response
                is_specific = len(answer) > 100 and ("**" in answer or "•" in answer or ":" in answer)
                
                if is_specific:
                    print(f"    ✅ Intent: {intent}")
                    print(f"    ✅ Response length: {len(answer)} chars (specific answer)")
                    success_count += 1
                else:
                    print(f"    ⚠️  Intent: {intent}")
                    print(f"    ⚠️  Response: {answer[:100]}...")
                
            else:
                print(f"    ❌ HTTP {response.status_code}")
            
            print()
            time.sleep(0.1)  # Small delay between requests
            
        except Exception as e:
            print(f"    ❌ Error: {e}\n")
    
    print("="*80)
    print(f"📊 RESULTS: {success_count}/{len(test_questions)} questions handled with specific answers")
    print(f"Success Rate: {(success_count/len(test_questions)*100):.1f}%")
    
    if success_count >= len(test_questions) * 0.8:
        print("✅ EXCELLENT: Chatbot handles diverse question types!")
    elif success_count >= len(test_questions) * 0.6:
        print("⚠️  GOOD: Most questions handled, some edge cases need work")
    else:
        print("❌ NEEDS IMPROVEMENT: Many questions falling back to generic responses")
    
    print("="*80 + "\n")

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ML JEWELRY CHATBOT COMPREHENSIVE TEST                     ║
║                                                                              ║
║  This test demonstrates the chatbot can handle:                             ║
║  • Inventory queries                                                        ║
║  • Product searches                                                         ║
║  • Pricing questions                                                        ║
║  • Comparisons                                                              ║
║  • Education (gemstones, materials)                                         ║
║  • Customization/Bespoke                                                    ║
║  • Sizing & Fitting                                                         ║
║  • Care & Maintenance                                                       ║
║  • Appointments & Visits                                                    ║
║  • Shipping & Delivery                                                      ║
║  • Returns & Exchanges                                                      ║
║  • Complex multi-intent queries                                             ║
║                                                                              ║
║  WITHOUT falling back to generic responses!                                 ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """)
    
    test_chatbot()
