"""
Simplified ML chatbot service for Ornament Tech
Uses the trained models to provide intelligent responses
"""
import os
import sys
import json
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from datetime import datetime
from sklearn.metrics.pairwise import cosine_similarity

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

app = Flask(__name__)
CORS(app)

class SimplifiedJewelryChatbot:
    def __init__(self):
        self.vectorizer = None
        self.response_data = None
        self.models_loaded = False
        self.confidence_threshold = 0.3
        
    def load_models(self):
        """Load vectorizer and response data"""
        try:
            models_dir = os.path.join(current_dir, 'models')
            
            # Load vectorizer
            vectorizer_path = os.path.join(models_dir, 'vectorizer.pkl')
            if os.path.exists(vectorizer_path):
                with open(vectorizer_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                    print("✓ Vectorizer loaded")
            
            # Load response data
            response_path = os.path.join(models_dir, 'response_data.pkl')
            if os.path.exists(response_path):
                with open(response_path, 'rb') as f:
                    self.response_data = pickle.load(f)
                    print("✓ Response data loaded")
            
            # Check if we have enough to work
            if self.vectorizer and self.response_data:
                self.models_loaded = True
                print("✓ ML models loaded successfully!")
                return True
            else:
                print("⚠ Some models missing, using fallback responses")
                return False
                
        except Exception as e:
            print(f"✗ Error loading models: {e}")
            return False
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        if not isinstance(text, str):
            return ""
        
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = ' '.join(text.split())
        return text
    
    def find_best_response(self, user_input):
        """Find best matching response using vectorizer"""
        if not self.models_loaded:
            return None, 0.0
            
        try:
            processed_input = self.preprocess_text(user_input)
            input_vector = self.vectorizer.transform([processed_input])
            
            # Calculate similarities
            similarities = cosine_similarity(
                input_vector, 
                self.response_data['question_vectors']
            )[0]
            
            best_match_idx = np.argmax(similarities)
            best_similarity = similarities[best_match_idx]
            
            if best_similarity > self.confidence_threshold:
                return self.response_data['responses'][best_match_idx], best_similarity
            
            return None, best_similarity
            
        except Exception as e:
            print(f"Error in similarity search: {e}")
            return None, 0.0
    
    def get_intent_from_keywords(self, user_input):
        """Simple keyword-based intent detection"""
        text = user_input.lower()
        
        if any(word in text for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return 'greeting'
        elif any(word in text for word in ['book', 'appointment', 'consultation', 'schedule']):
            return 'booking'
        elif any(word in text for word in ['price', 'cost', 'budget', 'expensive', 'cheap']):
            return 'pricing'
        elif any(word in text for word in ['material', 'metal', 'gold', 'platinum', 'silver']):
            return 'materials'
        elif any(word in text for word in ['diamond', 'gemstone', 'ruby', 'sapphire', 'emerald']):
            return 'gemstones'
        elif any(word in text for word in ['engagement', 'wedding', 'ring', 'band']):
            return 'product_info'
        elif any(word in text for word in ['process', 'bespoke', 'custom', 'how']):
            return 'process'
        elif any(word in text for word in ['thank', 'thanks']):
            return 'thanks'
        elif any(word in text for word in ['bye', 'goodbye', 'see you']):
            return 'goodbye'
        else:
            return 'unknown'
    
    def get_fallback_response(self, intent):
        """Get fallback responses based on intent"""
        responses = {
            "greeting": "Hello! Welcome to Ornament Tech. I'm your personal jewelry consultant, here to help you discover the perfect piece. Whether you're looking for an engagement ring, wedding bands, or a special gift, I can guide you through our collections and bespoke design process. What brings you here today?",
            
            "booking": "I'd love to help you schedule a personal consultation! We offer both in-person appointments at our London studio and virtual consultations worldwide. During your consultation, you'll work with our expert designers to explore options, see gemstones up close, and discuss your vision. You can book through our website at /appointments, call us, or I can provide you with our contact details.",
            
            "product_info": "We specialize in creating exceptional jewelry pieces, particularly engagement rings and wedding bands. Our engagement collection features classic solitaires, romantic halos, vintage-inspired designs, and completely custom creations. Each piece is handcrafted using the finest materials - 18k gold, platinum, and carefully selected diamonds and gemstones. Would you like to explore specific styles or learn about our customization options?",
            
            "pricing": "Our jewelry is investment-quality with pricing that reflects the finest materials and expert craftsmanship. Engagement rings typically range from £2,500 to £15,000+, wedding bands from £800 to £3,000+, and fine jewelry varies by design complexity. We work with various budgets and can guide you to the best value within your range. For detailed pricing, I'd recommend a consultation where we can discuss options specific to your needs.",
            
            "materials": "We work exclusively with premium materials to ensure lasting beauty and durability. Our metals include 18k gold in yellow, white, and rose options, plus platinum for the ultimate in luxury and hypoallergenic properties. Each metal has unique characteristics - platinum is naturally white and incredibly durable, gold offers warmth and tradition, and rose gold provides a romantic, contemporary appeal. Which metal interests you most?",
            
            "gemstones": "Our gemstone collection is truly exceptional. We specialize in diamonds graded by the 4 Cs (Cut, Color, Clarity, Carat), sourced ethically and selected for maximum brilliance. We also work with magnificent colored stones including sapphires, emeralds, rubies, and other precious gems. Each stone is hand-selected for its beauty and quality. Are you interested in learning about diamonds, colored stones, or a specific gemstone?",
            
            "process": "Our bespoke design process is what sets us apart. It begins with a personal consultation where we understand your vision and preferences. Then our designers create detailed sketches and 3D renderings for your approval. Once finalized, our master craftsmen handcraft your piece using traditional techniques. Throughout the process, you'll receive updates and photos. The typical timeline is 4-6 weeks, and the experience is as memorable as the final piece. Would you like to start with a consultation?",
            
            "thanks": "You're very welcome! I'm delighted to help you explore the world of fine jewelry. Is there anything specific about our collections, the design process, or booking a consultation that you'd like to know more about?",
            
            "goodbye": "Thank you for visiting Ornament Tech! Remember, we're here whenever you're ready to explore our collections or discuss your jewelry dreams. Have a wonderful day!",
            
            "unknown": "I'd be happy to help you with any questions about our jewelry collections, bespoke design process, materials, or booking a consultation. Could you tell me a bit more about what you're looking for? Are you interested in engagement rings, wedding bands, fine jewelry, or would you like to learn about our design process?"
        }
        
        return responses.get(intent, responses["unknown"])
    
    def generate_response(self, user_input):
        """Generate intelligent response"""
        # Try ML-based similarity matching first
        response, similarity = self.find_best_response(user_input)
        
        if response and similarity > self.confidence_threshold:
            return {
                "response": response,
                "method": "ml_similarity",
                "confidence": float(similarity),
                "intent": "matched",
                "timestamp": datetime.now().isoformat()
            }
        
        # Fall back to keyword-based intent detection
        intent = self.get_intent_from_keywords(user_input)
        fallback_response = self.get_fallback_response(intent)
        
        return {
            "response": fallback_response,
            "method": "keyword_intent", 
            "confidence": 0.8 if intent != "unknown" else 0.3,
            "intent": intent,
            "timestamp": datetime.now().isoformat()
        }

# Global chatbot instance
chatbot = SimplifiedJewelryChatbot()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Ornament Tech ML Chatbot",
        "models_loaded": chatbot.models_loaded
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
    print("🚀 Starting Ornament Tech ML Chatbot Service...")
    
    # Load models
    if chatbot.load_models():
        print("✅ ML models ready!")
    else:
        print("⚠️  Running without full ML models - using keyword fallbacks")
    
    print("🌐 Starting server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)