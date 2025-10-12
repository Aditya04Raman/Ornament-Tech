import json
import os
import random
import sys

# Add the utils directory to the path to import website_scraper
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from website_scraper import extract_website_content

def generate_training_data():
    """
    Generate training data for the ML chatbot based on website content
    """
    
    # Get website content
    content = extract_website_content()
    
    training_data = []
    
    # Brand and general info
    brand_questions = [
        ("What is Ornament Tech?", f"{content['brand']['name']} is {content['brand']['description']} We specialize in {content['brand']['tagline']}."),
        ("Tell me about your company", f"We are {content['brand']['name']} with {content['brand']['experience']} of experience. We've created {content['brand']['pieces_created']} for {content['brand']['customers']}."),
        ("What are your values?", f"Our core values are {', '.join(content['brand']['values'])}. These guide everything we do in creating exceptional jewelry."),
        ("How long have you been in business?", f"We have {content['brand']['experience']} of experience in bespoke jewelry creation."),
        ("How many customers have you served?", f"We've proudly served {content['brand']['customers']} and created {content['brand']['pieces_created']}."),
    ]
    training_data.extend(brand_questions)
    
    # Bespoke process questions
    process_questions = [
        ("How does the bespoke process work?", f"{content['bespoke_process']['overview']} Our process has 4 main steps: Consultation, Design, Craft, and Delivery."),
        ("How long does the bespoke process take?", f"The bespoke process {content['bespoke_process']['typical_timeline']}."),
        ("What happens in the consultation?", f"Step 1 - Consultation: {content['bespoke_process']['steps'][0]['description']}"),
        ("Tell me about the design phase", f"Step 2 - Design: {content['bespoke_process']['steps'][1]['description']}"),
        ("How is my jewelry crafted?", f"Step 3 - Craft: {content['bespoke_process']['steps'][2]['description']}"),
        ("When will I receive my jewelry?", f"Step 4 - Delivery: {content['bespoke_process']['steps'][3]['description']}"),
    ]
    training_data.extend(process_questions)
    
    # Collection questions
    for collection in content['collections']:
        collection_questions = [
            (f"Tell me about {collection['name']}", f"{collection['name']}: {collection['description']} We have {collection['pieces']} available, starting {collection['starting_price']}."),
            (f"What {collection['name'].lower()} do you have?", f"Our {collection['name']} collection includes {', '.join(collection.get('styles', []))}. {collection['description']}"),
            (f"How much for {collection['name'].lower()}?", f"{collection['name']} start {collection['starting_price']}. Prices vary based on materials and complexity."),
        ]
        training_data.extend(collection_questions)
    
    # Material questions
    for material in content['materials']:
        material_questions = [
            (f"Tell me about {material['name']}", f"{material['name']}: {material['description']} Key properties: {', '.join(material['properties'])}."),
            (f"What are the benefits of {material['name']}?", f"{material['name']} offers {', '.join(material['properties'])}. It's best for {material['best_for']}."),
            (f"How durable is {material['name']}?", f"{material['name']} has {material['durability']} durability and requires {material['maintenance']} maintenance."),
        ]
        training_data.extend(material_questions)
    
    # Gemstone questions
    for gemstone in content['gemstones']:
        gemstone_questions = [
            (f"Tell me about {gemstone['name']}", f"{gemstone['name']}: {gemstone['description']} Key characteristics: {', '.join(gemstone['characteristics'])}."),
            (f"What makes {gemstone['name']} special?", f"{gemstone['name']} are valued for {', '.join(gemstone['characteristics'])}."),
        ]
        training_data.extend(gemstone_questions)
    
    # Service questions
    service_questions = [
        ("How do I book a consultation?", f"You can book a {', '.join(content['services']['consultations']['types'])}. We offer {content['services']['consultations']['cost']} and typical sessions last {content['services']['consultations']['duration']}."),
        ("Where are your locations?", f"We have locations in {', '.join([loc['name'] for loc in content['locations']])}. Our main studio is in {content['locations'][0]['address']}."),
        ("Do you offer virtual consultations?", f"Yes! We offer {', '.join(content['services']['consultations']['types'])}. Virtual consultations are a great way to start your bespoke journey from anywhere."),
        ("What should I expect in a consultation?", f"During your consultation: {' '.join(content['services']['consultations']['what_to_expect'])}."),
    ]
    training_data.extend(service_questions)
    
    # Pricing questions
    pricing_questions = [
        ("What are your prices?", "Our prices vary by collection: Engagement rings from £2,500, Wedding bands from £800, Necklaces from £1,200, Earrings from £600. We work with all budgets."),
        ("Do you offer payment plans?", f"Yes, we offer {', '.join(content['pricing']['payment_options'])} to make your dream piece more accessible."),
        ("Is there a consultation fee?", f"No, we offer {content['services']['consultations']['cost']}. All initial consultations are complimentary."),
    ]
    training_data.extend(pricing_questions)
    
    # FAQ questions
    for faq in content['faq']:
        training_data.append((faq['question'], faq['answer']))
    
    # Contact questions
    contact_questions = [
        ("How can I contact you?", f"You can reach us at {content['contact']['email']}, call {content['contact']['phone']}, or use our WhatsApp. We respond {content['contact']['response_time']}."),
        ("What are your hours?", f"We're available {content['contact']['availability']}. You can also reach us anytime through our AI concierge."),
        ("Do you have social media?", f"Yes! Follow us on Instagram {content['contact']['social_media']['instagram']}, Facebook {content['contact']['social_media']['facebook']}, and Pinterest {content['contact']['social_media']['pinterest']}."),
    ]
    training_data.extend(contact_questions)
    
    # Care and maintenance questions
    care_questions = [
        ("How do I care for my jewelry?", "Clean gently with warm water and mild soap. Store in individual pouches to prevent scratching. We recommend annual professional check-ups."),
        ("Do you offer repairs?", "Yes, we offer comprehensive repair services, resizing, cleaning, and maintenance. We provide a lifetime guarantee on our craftsmanship."),
        ("Can you resize my ring?", "Yes, we offer resizing services. Most rings can be resized up or down by 2-3 sizes, though complex designs may have limitations."),
    ]
    training_data.extend(care_questions)
    
    # Intent-based variations
    intent_variations = []
    for question, answer in training_data[:]:
        # Add greeting variations
        greetings = ["Hi, ", "Hello, ", "Hey, ", "Good morning, ", "Good afternoon, "]
        for greeting in greetings:
            intent_variations.append((greeting + question.lower(), answer))
        
        # Add question variations
        question_starters = ["Can you tell me ", "I'd like to know ", "I'm interested in ", "Could you explain "]
        for starter in question_starters:
            if question.startswith(("What", "How", "Tell me")):
                new_question = starter + question.lower()
                intent_variations.append((new_question, answer))
    
    # Add some of the variations (to avoid too much data)
    training_data.extend(random.sample(intent_variations, min(100, len(intent_variations))))
    
    # Save training data
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'training-data.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            "training_pairs": training_data,
            "total_samples": len(training_data),
            "categories": ["brand", "bespoke_process", "collections", "materials", "gemstones", "services", "pricing", "faq", "contact", "care"]
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Generated {len(training_data)} training samples and saved to {output_path}")
    return training_data

def generate_intent_data():
    """
    Generate intent classification data
    """
    intents = {
        "greeting": [
            "hello", "hi", "hey", "good morning", "good afternoon", "good evening",
            "howdy", "greetings", "what's up", "how are you"
        ],
        "booking": [
            "book appointment", "schedule consultation", "make appointment", "book consultation",
            "schedule meeting", "arrange consultation", "book session", "reserve appointment"
        ],
        "product_info": [
            "tell me about", "what is", "describe", "explain", "information about",
            "details about", "learn about", "know about", "show me"
        ],
        "pricing": [
            "how much", "what's the price", "cost", "pricing", "budget", "expensive",
            "affordable", "payment", "price range", "what does it cost"
        ],
        "materials": [
            "gold", "platinum", "silver", "metal", "material", "what's it made of",
            "rose gold", "white gold", "yellow gold", "metals"
        ],
        "gemstones": [
            "diamond", "sapphire", "emerald", "ruby", "gemstone", "stone", "gem",
            "precious stone", "birthstone", "crystal"
        ],
        "process": [
            "how does it work", "process", "steps", "procedure", "method", "how do you",
            "what happens", "timeline", "stages", "workflow"
        ],
        "contact": [
            "contact", "phone", "email", "address", "location", "where are you",
            "how to reach", "get in touch", "call", "visit"
        ],
        "care": [
            "care", "maintenance", "clean", "repair", "resize", "fix", "polish",
            "look after", "maintain", "service"
        ],
        "thanks": [
            "thank you", "thanks", "appreciate", "grateful", "cheers", "ta",
            "much appreciated", "thank you so much"
        ],
        "goodbye": [
            "goodbye", "bye", "see you", "farewell", "take care", "catch you later",
            "talk to you later", "have a good day"
        ]
    }
    
    # Save intent data
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'intents.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(intents, f, indent=2, ensure_ascii=False)
    
    print(f"Generated intent data and saved to {output_path}")
    return intents

if __name__ == "__main__":
    generate_training_data()
    generate_intent_data()
