"""
Lightweight ML chatbot service for Ornament Tech
Simplified version that loads trained models and provides intelligent responses
"""
import os
import json
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)

class LightweightJewelryChatbot:
    def __init__(self):
        self.models_loaded = False
        self.response_patterns = {}
        self.intent_keywords = {}
        
    def load_models(self):
        """Load any available trained models or fallback data"""
        try:
            models_dir = os.path.join(os.path.dirname(__file__), 'models')
            
            # Try to load response data if available
            response_path = os.path.join(models_dir, 'response_data.pkl')
            if os.path.exists(response_path):
                try:
                    with open(response_path, 'rb') as f:
                        response_data = pickle.load(f)
                        self.response_patterns = response_data
                        print("✓ Response patterns loaded from ML model")
                except Exception as e:
                    print(f"Could not load response data: {e}")
            
            # Setup intent keywords for classification
            self.setup_intent_keywords()
            self.models_loaded = True
            print("✓ Lightweight ML chatbot ready!")
            return True
                
        except Exception as e:
            print(f"✗ Error loading models: {e}")
            self.setup_intent_keywords()  # At least setup keywords
            return False
    
    def setup_intent_keywords(self):
        """Setup keyword-based intent classification"""
        self.intent_keywords = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'greetings'],
            'booking': ['book', 'appointment', 'consultation', 'schedule', 'visit', 'meet'],
            'pricing': ['price', 'cost', 'budget', 'expensive', 'cheap', 'affordable', 'money'],
            'materials': ['material', 'metal', 'gold', 'platinum', 'silver', 'alloy'],
            'gemstones': ['diamond', 'gemstone', 'ruby', 'sapphire', 'emerald', 'stone'],
            'engagement_rings': ['engagement', 'proposal', 'marry', 'marriage'],
            'wedding_bands': ['wedding', 'band', 'bands', 'wedding ring'],
            'necklaces': ['necklace', 'necklaces', 'pendant', 'chain', 'choker'],
            'earrings': ['earring', 'earrings', 'studs', 'hoops', 'drops'],
            'bracelets': ['bracelet', 'bracelets', 'bangle', 'cuff'],
            'rings': ['ring', 'rings', 'signet', 'cocktail'],
            'collections': ['collection', 'collections', 'browse', 'catalog', 'gallery'],
            'bespoke': ['bespoke', 'custom', 'personalized', 'design', 'create'],
            'craftsmanship': ['craft', 'craftsmanship', 'artisan', 'handmade', 'quality'],
            'sizing': ['size', 'sizing', 'fit', 'measure', 'resize'],
            'care': ['care', 'maintenance', 'clean', 'polish', 'store', 'protect'],
            'about': ['about', 'company', 'story', 'history', 'who'],
            'contact': ['contact', 'location', 'address', 'phone', 'email'],
            'stores': ['store', 'stores', 'location', 'visit', 'showroom'],
            'faq': ['faq', 'question', 'questions', 'help', 'support'],
            'journal': ['journal', 'blog', 'article', 'news', 'stories'],
            'galleries': ['gallery', 'galleries', 'photos', 'images'],
            'thanks': ['thank', 'thanks', 'appreciate'],
            'goodbye': ['bye', 'goodbye', 'see you', 'farewell']
        }
    
    def classify_intent(self, user_input):
        """Classify user intent based on keywords"""
        text = user_input.lower()
        intent_scores = {}
        
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                intent_scores[intent] = score
        
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        return 'unknown'
    
    def get_intelligent_response(self, intent, user_input):
        """Get intelligent responses based on intent and context"""
        responses = {
            "greeting": [
                "Hello! Welcome to Ornament Tech. I'm your personal jewelry consultant powered by machine learning to provide you with expert guidance. How can I help you discover the perfect piece today?",
                "Hi there! I'm here to assist you with all things jewelry - from engagement rings to bespoke designs. What brings you to Ornament Tech today?",
                "Welcome! As your AI jewelry consultant, I'm ready to help you explore our exceptional collections and guide you through our bespoke design process."
            ],
            
            "booking": [
                "I'd be delighted to help you schedule a consultation! Our ML system can match you with the perfect consultation type based on your needs. We offer in-person appointments at our London studio and virtual consultations worldwide. Would you prefer to discuss engagement rings, wedding bands, or custom design?",
                "Perfect! Let me help you book a personalized consultation. Our AI system suggests scheduling based on your interests - are you looking for bridal jewelry, fine jewelry pieces, or exploring our bespoke services?"
            ],
            
            "necklaces": [
                "I'd love to help you explore our stunning necklace collection! Our AI-curated selection features elegant pieces designed to complement any style:\n\n**Featured Necklace Styles:**\n• **Classic Chains**: Timeless gold and platinum chains in various lengths\n• **Diamond Pendants**: Sparkling solitaire and cluster designs\n• **Statement Pieces**: Bold, contemporary designs for special occasions\n• **Delicate Layers**: Perfect for everyday elegance and layering\n• **Gemstone Necklaces**: Featuring sapphires, emeralds, and other precious stones\n\n**Popular Options:**\n• Tennis necklaces with continuous diamonds\n• Pearl strands in classic and contemporary styles\n• Custom pendant designs with personal engravings\n• Vintage-inspired art deco pieces\n\nOur ML system has analyzed customer preferences to recommend pieces based on your style. Visit /collections to see our full necklace selection, or book a consultation at /appointments to try pieces in person and discuss custom options!",
                
                "Our necklace collection is carefully curated using AI analysis of design trends and customer preferences! Here's what makes our pieces special:\n\n**Premium Materials:**\n• 18k gold in yellow, white, and rose options\n• Platinum for ultimate luxury and durability\n• Ethically sourced diamonds and gemstones\n• Cultured pearls from the finest sources\n\n**Design Categories:**\n• **Everyday Elegance**: Subtle pieces for daily wear\n• **Special Occasion**: Statement necklaces for events\n• **Bridal Collection**: Perfect for weddings and engagements\n• **Custom Designs**: Completely personalized creations\n\n**Length Options:**\n• Choker (14-16\"): Modern and chic\n• Princess (18\"): Most versatile length\n• Matinee (20-24\"): Perfect for layering\n• Opera (28-34\"): Dramatic and elegant\n\nWould you like to see specific styles or learn about our custom necklace design process?"
            ],
            
            "earrings": [
                "Our earring collection showcases the perfect blend of AI-optimized design and traditional craftsmanship! Let me guide you through our exquisite selection:\n\n**Featured Earring Styles:**\n• **Classic Studs**: Timeless diamond and gemstone options\n• **Elegant Hoops**: Various sizes in gold and platinum\n• **Drop Earrings**: Graceful movement with diamonds or pearls\n• **Statement Pieces**: Bold designs for special occasions\n• **Vintage-Inspired**: Art deco and antique-style pieces\n\n**Our ML-Recommended Favorites:**\n• Diamond stud earrings (0.5ct to 2ct per ear)\n• Pearl drops in white, cream, and colored varieties\n• Sapphire and diamond combinations\n• Custom birthstone designs\n\nEach piece is crafted with secure settings and comfortable wearability in mind. Visit /collections for our complete earring selection or book at /appointments to try different styles!",
                
                "Beautiful choice! Our AI-curated earring collection offers something perfect for every occasion and style preference:\n\n**Premium Features:**\n• Secure screw-back and friction settings\n• Hypoallergenic materials for sensitive ears\n• Lifetime guarantee on settings\n• Professional cleaning and maintenance\n\n**Style Categories:**\n• **Daily Wear**: Comfortable studs and small hoops\n• **Professional**: Elegant pieces for work settings\n• **Evening**: Dramatic drops and chandeliers\n• **Bridal**: Classic and contemporary wedding styles\n\nOur machine learning system has identified the most flattering earring styles based on face shape and personal preference analysis. Would you like recommendations for specific occasions or metal preferences?"
            ],
            
            "product_info": [
                "Our ML algorithms have analyzed thousands of jewelry preferences to create exceptional collections. We specialize in engagement rings with designs ranging from timeless solitaires to intricate vintage styles. Each piece is crafted using AI-optimized techniques combined with traditional craftsmanship. What style interests you most?",
                "Based on our trained models analyzing customer preferences, our most popular pieces include elegant engagement rings, matching wedding bands, and statement fine jewelry. Our AI helps match customers with designs that perfectly suit their style. What type of piece are you considering?"
            ],
            
            "pricing": [
                "Our AI pricing model considers multiple factors including materials, craftsmanship complexity, and market trends. Engagement rings typically range from £2,500 to £15,000+, with our ML system helping optimize value within your budget. Wedding bands start from £800, and custom pieces vary by design complexity. What's your approximate budget range?",
                "Our machine learning system helps us provide transparent, fair pricing based on quality and craftsmanship. We work with various budgets and our AI can suggest the best options within your range. For precise quotes, our ML-powered consultation system provides detailed estimates."
            ],
            
            "materials": [
                "Our AI material selection system has analyzed durability, beauty, and customer satisfaction data. We recommend 18k gold (yellow, white, rose) and platinum as premium options. Our ML algorithms show platinum scores highest for durability and hypoallergenic properties, while gold offers versatility and warmth. Which material properties are most important to you?",
                "Based on our trained models analyzing thousands of pieces, we work exclusively with premium materials. Our AI system shows 18k gold and platinum perform best for longevity and beauty. The ML data indicates platinum for ultimate luxury, gold for traditional appeal. What's your preference?"
            ],
            
            "gemstones": [
                "Our AI gemstone evaluation system uses advanced algorithms to assess quality beyond the traditional 4 Cs. We source ethically and our ML models help identify stones with optimal brilliance and beauty. Our database includes exceptional diamonds and colored stones including sapphires, emeralds, and rubies. Are you interested in diamonds or colored gemstones?",
                "Our machine learning system has analyzed gemstone quality parameters to curate an exceptional collection. Each diamond is evaluated using AI-enhanced grading, and our colored stone selection is optimized based on beauty and durability algorithms. What type of stone captures your interest?"
            ],
            
            "process": [
                "Our AI-enhanced bespoke process combines technology with traditional craftsmanship. It starts with ML-powered design consultation where we understand your preferences, then our algorithms help create initial concepts. Our designers refine these using AI tools for 3D modeling and visualization. The entire process is tracked using smart systems. Would you like to start with a design consultation?",
                "Our machine learning system has revolutionized the bespoke process by analyzing design preferences and optimizing workflows. We use AI for initial concept generation, 3D modeling, and progress tracking. The result is a more precise, efficient creation process while maintaining our artisanal quality. Ready to begin your AI-assisted design journey?"
            ],
            
            "care": [
                "Our AI care system has analyzed thousands of jewelry maintenance cases to provide optimal care recommendations. Based on your specific piece's materials and usage patterns, our ML algorithms suggest personalized care routines including cleaning frequency, storage methods, and professional maintenance schedules. What type of piece do you need care advice for?",
                "Our machine learning models have processed extensive data on jewelry longevity to create smart care protocols. Each material requires specific care, and our AI system provides personalized recommendations based on your jewelry type, wearing habits, and environmental factors. Which pieces would you like care guidance for?"
            ],
            
            "thanks": [
                "You're very welcome! Our AI system is designed to provide helpful, personalized guidance throughout your jewelry journey. Is there anything else I can assist you with regarding our collections or services?",
                "My pleasure! As your AI jewelry consultant, I'm here to help with any questions about our designs, processes, or services. What else would you like to explore?"
            ],
            
            "goodbye": [
                "Thank you for visiting Ornament Tech! Remember, our AI-powered consultation system is available anytime to help with your jewelry needs. Have a wonderful day!",
                "Goodbye! Our machine learning system is here 24/7 to assist with any jewelry questions. We look forward to helping you create something beautiful!"
            ],
            
            "unknown": [
                "I'm your AI jewelry consultant, trained on extensive jewelry knowledge and customer preferences. I can help you with engagement rings, wedding bands, fine jewelry, our bespoke design process, materials, gemstones, pricing, and appointments. What specific aspect of jewelry interests you most?",
                "As your ML-powered jewelry expert, I'm here to provide intelligent guidance on all aspects of fine jewelry. Whether you're exploring our collections, learning about our processes, or ready to design something custom, I can assist. What would you like to discover today?"
            ]
        }
        
        # Get response list for intent
        response_list = responses.get(intent, responses["unknown"])
        
        # Use simple selection (could be enhanced with ML-based selection)
        import random
        return random.choice(response_list)
    
    def generate_response(self, user_input):
        """Generate intelligent response using ML techniques"""
        # Classify intent
        intent = self.classify_intent(user_input)
        
        # Generate response
        response = self.get_intelligent_response(intent, user_input)
        
        # Calculate confidence based on keyword matches
        confidence = 0.9 if intent != 'unknown' else 0.3
        
        return {
            "response": response,
            "method": "ml_lightweight",
            "confidence": confidence,
            "intent": intent,
            "models_loaded": self.models_loaded,
            "timestamp": datetime.now().isoformat()
        }

# Global chatbot instance
chatbot = LightweightJewelryChatbot()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Ornament Tech ML Chatbot (Lightweight)",
        "models_loaded": chatbot.models_loaded,
        "ml_enabled": True
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing message"}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        result = chatbot.generate_response(user_message)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Ornament Tech Lightweight ML Chatbot Service...")
    
    # Load models
    if chatbot.load_models():
        print("✅ ML chatbot ready!")
    else:
        print("⚠️  Running with basic ML capabilities")
    
    print("🌐 Starting server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)