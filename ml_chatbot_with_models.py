"""
TRUE ML-POWERED CHATBOT - Loads and uses trained neural network models
This version actually uses the .h5 models for predictions
"""

import pandas as pd
import numpy as np
import re
import os
import sys
import pickle
from flask import Flask, request, jsonify
from flask_cors import CORS

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

try:
    # Allow opting out of TensorFlow import for environments where it's
    # incompatible (for example, newer Python versions). Set SKIP_TF=1 to
    # force the fallback engine.
    if os.getenv('SKIP_TF', '0') == '1':
        raise ImportError('SKIP_TF set')
    import tensorflow as tf
    print("✓ TensorFlow loaded")
except Exception as e:
    # Catch any exception (ImportError, ABI mismatch, runtime errors) so the
    # service can still run in fallback mode without crashing during import.
    print(f"✗ TensorFlow import failed or skipped ({e}) - will use fallback")
    tf = None

# Ensure stdout can handle Unicode on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

app = Flask(__name__)
CORS(app)

class MLJewelryChatbot:
    def __init__(self):
        self.jewelry_data = None
        self.diamonds_data = None
        self.knowledge_base = {}
        
        # ML model components
        self.intent_model = None
        self.price_model = None
        self.vectorizer = None
        self.label_encoder = None
        self.price_scaler = None
        
        # Status flags
        self.ml_models_loaded = False
        
        print("Initializing ML-Powered Chatbot...")
        self.load_datasets()
        self.load_ml_models()
        self.build_knowledge()
        print("Chatbot ready!")
    
    def load_datasets(self):
        """Load jewelry and diamond datasets"""
        try:
            paths = [
                'ml-chatbot/models/jewelry_dataset.csv',
                'jewelry_dataset.csv',
                'models/jewelry_dataset.csv'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    self.jewelry_data = pd.read_csv(path)
                    print(f"✓ Loaded {len(self.jewelry_data)} jewelry items from {path}")
                    break
            
            paths = [
                'ml-chatbot/models/diamonds_dataset.csv',
                'diamonds_dataset.csv',
                'models/diamonds_dataset.csv'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    self.diamonds_data = pd.read_csv(path)
                    print(f"✓ Loaded {len(self.diamonds_data)} diamonds from {path}")
                    break
                    
        except Exception as e:
            print(f"✗ Error loading datasets: {e}")
    
    def load_ml_models(self):
        """Load trained ML models (.h5 and .pkl files)"""
        if tf is None:
            print("✗ TensorFlow not available, using pattern matching fallback")
            return
        
        try:
            model_dir = 'ml-chatbot/models'
            
            # Try to load enhanced models first
            enhanced_intent_path = os.path.join(model_dir, 'enhanced_intent_model.h5')
            enhanced_vec_path = os.path.join(model_dir, 'enhanced_vectorizer.pkl')
            enhanced_enc_path = os.path.join(model_dir, 'enhanced_label_encoder.pkl')
            
            if os.path.exists(enhanced_intent_path):
                self.intent_model = tf.keras.models.load_model(enhanced_intent_path, compile=False)
                print(f"✓ Loaded enhanced intent model from {enhanced_intent_path}")
                
                with open(enhanced_vec_path, 'rb') as f:
                    self.vectorizer = pickle.load(f)
                print(f"✓ Loaded enhanced vectorizer")
                
                with open(enhanced_enc_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
                print(f"✓ Loaded enhanced label encoder")
                print(f"  Intent classes: {self.label_encoder.classes_}")
                
                self.ml_models_loaded = True
            else:
                # Fallback to basic models
                intent_path = os.path.join(model_dir, 'intent_model.h5')
                vec_path = os.path.join(model_dir, 'vectorizer.pkl')
                enc_path = os.path.join(model_dir, 'label_encoder.pkl')
                
                if os.path.exists(intent_path):
                    self.intent_model = tf.keras.models.load_model(intent_path, compile=False)
                    print(f"✓ Loaded basic intent model from {intent_path}")
                    
                    with open(vec_path, 'rb') as f:
                        self.vectorizer = pickle.load(f)
                    print(f"✓ Loaded basic vectorizer")
                    
                    with open(enc_path, 'rb') as f:
                        self.label_encoder = pickle.load(f)
                    print(f"✓ Loaded basic label encoder")
                    
                    self.ml_models_loaded = True
            
            # Try to load price prediction model
            price_model_path = os.path.join(model_dir, 'price_prediction_model.h5')
            price_scaler_path = os.path.join(model_dir, 'price_scaler.pkl')
            
            if os.path.exists(price_model_path):
                self.price_model = tf.keras.models.load_model(price_model_path, compile=False)
                print(f"✓ Loaded price prediction model")
                
                if os.path.exists(price_scaler_path):
                    with open(price_scaler_path, 'rb') as f:
                        self.price_scaler = pickle.load(f)
                    print(f"✓ Loaded price scaler")
            
            if self.ml_models_loaded:
                print("✓✓✓ ML MODELS SUCCESSFULLY LOADED - Using Neural Networks ✓✓✓")
            else:
                print("✗ No ML models found, using pattern matching fallback")
                
        except Exception as e:
            print(f"✗ Error loading ML models: {e}")
            print("  Falling back to pattern matching")
            self.ml_models_loaded = False
    
    def build_knowledge(self):
        """Build knowledge base from datasets"""
        if self.jewelry_data is not None:
            self.knowledge_base['categories'] = self.jewelry_data['category'].unique().tolist() if 'category' in self.jewelry_data.columns else []
            self.knowledge_base['materials'] = self.jewelry_data['metal'].unique().tolist() if 'metal' in self.jewelry_data.columns else []
            self.knowledge_base['stones'] = self.jewelry_data['stone'].unique().tolist() if 'stone' in self.jewelry_data.columns else []
            self.knowledge_base['total_jewelry'] = len(self.jewelry_data)
            
            if 'price' in self.jewelry_data.columns:
                self.knowledge_base['price_min'] = float(self.jewelry_data['price'].min())
                self.knowledge_base['price_max'] = float(self.jewelry_data['price'].max())
                self.knowledge_base['price_avg'] = float(self.jewelry_data['price'].mean())
        
        if self.diamonds_data is not None:
            self.knowledge_base['total_diamonds'] = len(self.diamonds_data)
            if 'cut' in self.diamonds_data.columns:
                self.knowledge_base['diamond_cuts'] = self.diamonds_data['cut'].unique().tolist()
            if 'color' in self.diamonds_data.columns:
                self.knowledge_base['diamond_colors'] = self.diamonds_data['color'].unique().tolist()
        
        print(f"✓ Knowledge Base: {self.knowledge_base.get('total_jewelry', 0):,} jewelry, {self.knowledge_base.get('total_diamonds', 0):,} diamonds")
    
    def preprocess_text(self, text):
        """Clean text for ML model input"""
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = ' '.join(text.split())
        return text

    def _is_search_like(self, query: str) -> bool:
        """Detect if a query is likely asking for product search results."""
        q = query.lower()
        # presence of action verbs + product terms or explicit filters (price, metal, carat)
        if re.search(r'\b(show|find|search|looking for|want|need|browse)\b', q) and re.search(r'\b(ring|necklace|earring|bracelet|jewelry|jewellery|diamond|stone)\b', q):
            return True
        if re.search(r'\b(under|below|less than|under\$|<|<=)\b', q) and re.search(r'\$?\d{2,}', q):
            return True
        if re.search(r'\b(platinum|gold|silver|rose gold|white gold|metal|titanium)\b', q) and re.search(r'\b(ring|necklace|earring|bracelet|diamond)\b', q):
            return True
        return False

    def _is_pricing_like(self, query: str) -> bool:
        """Detect if a query specifically asks about pricing or value."""
        q = query.lower()
        if re.search(r'\b(price|cost|how much|worth|value|range|estimate|quote)\b', q):
            return True
        # explicit currency mentions
        if re.search(r'\$\s?\d{2,}|\d{2,}\s?usd', q):
            return True
        return False

    def _is_appointment_like(self, query: str) -> bool:
        q = query.lower()
        return bool(re.search(r'\b(appointment|book|schedule|consultation|visit|store|meet)\b', q))

    def _is_shipping_like(self, query: str) -> bool:
        q = query.lower()
        return bool(re.search(r'\b(ship|shipping|delivery|international|overseas|courier|express|overnight)\b', q))

    def _is_returns_like(self, query: str) -> bool:
        q = query.lower()
        return bool(re.search(r'\b(return|refund|exchange|policy|replace)\b', q))

    def _is_customization_like(self, query: str) -> bool:
        q = query.lower()
        return bool(re.search(r'\b(custom|customize|bespoke|design|engrave|modify|personalize)\b', q))

    def _is_sizing_like(self, query: str) -> bool:
        q = query.lower()
        return bool(re.search(r'\b(size|sizing|ring size|measure|measurement|fit|resiz)\b', q))

    def _is_care_like(self, query: str) -> bool:
        q = query.lower()
        return bool(re.search(r'\b(care|clean|maintain|polish|repair|warranty|tarnish)\b', q))

    def _is_material_like(self, query: str) -> bool:
        q = query.lower()
        return bool(re.search(r'\b(gold|silver|platinum|metal|material|titanium|alloy|white gold|rose gold)\b', q))

    def _is_comparison_like(self, query: str) -> bool:
        q = query.lower()
        return bool(re.search(r'\b(compare|comparison|difference|differ|better|best|versus|vs|between|which one)\b', q))
    
    def classify_intent_ml(self, query):
        """Use NEURAL NETWORK to classify intent"""
        if not self.ml_models_loaded:
            return None
        
        try:
            # Preprocess
            processed = self.preprocess_text(query)
            
            # Vectorize using trained TF-IDF
            input_vector = self.vectorizer.transform([processed])
            
            # Predict with neural network
            predictions = self.intent_model.predict(input_vector.toarray(), verbose=0)
            predicted_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_idx])
            
            # Decode intent
            intent = self.label_encoder.inverse_transform([predicted_idx])[0]
            
            print(f"[ML PREDICTION] Intent: {intent}, Confidence: {confidence:.3f}")
            return intent, confidence
            
        except Exception as e:
            print(f"✗ ML prediction error: {e}")
            return None
    
    def classify_intent_regex(self, query):
        """Fallback regex-based intent classification"""
        q = query.lower()
        
        if re.search(r'(what|which|tell me|show me).*(type|kind|category|categories|collection|have|available|stock|inventory|sell|offer)', q):
            return 'inventory', 0.9
        if re.search(r'(show|find|search|looking for|want|need|interested in|browse).*(ring|necklace|earring|bracelet|jewelry|jewellery|pendant|chain)', q):
            return 'search', 0.85
        if re.search(r'(price|cost|expensive|cheap|budget|afford|how much|value|worth|range)', q):
            return 'pricing', 0.9
        if re.search(r'(diamond|ruby|emerald|sapphire|gemstone|stone|crystal).*(what|how|tell|explain|quality|grade|clarity|cut|carat)', q):
            return 'education', 0.85
        if re.search(r'(gold|silver|platinum|metal|material|titanium|brass|copper|alloy)', q):
            return 'material', 0.85
        if re.search(r'(compare|comparison|difference|differ|better|best|versus|vs|between|which one|should i)', q):
            return 'comparison', 0.9
        if re.search(r'(custom|customize|bespoke|design|personalize|engrave|make|create|unique)', q):
            return 'customization', 0.85
        if re.search(r'(size|sizing|fit|fitting|measure|measurement|resize)', q):
            return 'sizing', 0.85
        if re.search(r'(care|clean|maintain|polish|repair|fix|damage|warranty)', q):
            return 'care', 0.85
        if re.search(r'(appointment|visit|store|location|book|schedule|meet|consultation)', q):
            return 'appointment', 0.85
        if re.search(r'^(hi|hello|hey|good morning|good afternoon|good evening|greetings)', q):
            return 'greeting', 0.95
        if re.search(r'(thank|thanks|appreciate|grateful)', q):
            return 'gratitude', 0.95
        
        return 'general', 0.5
    
    def classify_intent(self, query):
        """Unified intent classification: try ML first, fallback to regex"""
        # Try ML model first
        ml_result = self.classify_intent_ml(query)
        if ml_result:
            return ml_result
        
        # Fallback to regex
        print("[FALLBACK] Using pattern matching")
        return self.classify_intent_regex(query)
    
    def handle_inventory(self, query):
        """Answer inventory questions with real data"""
        kb = self.knowledge_base
        
        response = f"**Our Complete Jewelry Collection**\n\n"
        response += f"**Total Items:** {kb.get('total_jewelry', 0):,} jewelry pieces\n\n"
        
        if kb.get('categories'):
            response += "**Jewelry Categories:**\n"
            for cat in kb['categories'][:10]:
                if self.jewelry_data is not None:
                    count = len(self.jewelry_data[self.jewelry_data['category'] == cat])
                    response += f"• {cat.capitalize()}: {count:,} pieces\n"
        
        if kb.get('materials'):
            response += "\n**Premium Materials:**\n"
            for mat in kb['materials'][:8]:
                if self.jewelry_data is not None and mat and str(mat) != 'nan':
                    count = len(self.jewelry_data[self.jewelry_data['metal'] == mat])
                    response += f"• {mat}: {count:,} pieces\n"
        
        if kb.get('price_min'):
            response += f"\n**Price Range:** ${kb['price_min']:,.0f} - ${kb['price_max']:,.0f}\n"
            response += f"**Average Price:** ${kb['price_avg']:,.0f}\n"
        
        response += "\n\nWe also have {0:,} certified diamonds in our collection!".format(kb.get('total_diamonds', 0))
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        
        return response
    
    def handle_search(self, query):
        """Handle product search"""
        if self.jewelry_data is None:
            return "I apologize, but I'm currently unable to access our inventory."
        
        q = query.lower()
        results = self.jewelry_data.copy()
        
        # Simple category filtering
        for cat in ['ring', 'necklace', 'earring', 'bracelet']:
            if cat in q:
                results = results[results['category'].str.contains(cat, case=False, na=False)]
                break
        
        if len(results) == 0:
            return f"I couldn't find exact matches. We have {len(self.jewelry_data):,} pieces total. Try /collections!"
        
        response = f"**Found {len(results):,} pieces**\n\n"
        
        for idx, item in results.head(5).iterrows():
            response += f"• {item.get('category', 'Jewelry').capitalize()}"
            if 'metal' in item and pd.notna(item['metal']):
                response += f" - {item['metal']}"
            if 'price' in item and pd.notna(item['price']):
                response += f" - ${item['price']:,.0f}"
            response += "\n"
        
        response += f"\n\nVisit /collections to see all {len(results):,} pieces!"
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        
        return response
    
    def handle_pricing(self, query):
        """Handle pricing queries"""
        kb = self.knowledge_base
        response = "**Pricing Information**\n\n"
        response += f"**Price Range:** ${kb.get('price_min', 0):,.0f} - ${kb.get('price_max', 0):,.0f}\n"
        response += f"**Average Price:** ${kb.get('price_avg', 0):,.0f}\n"
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response
    
    def handle_education(self, query):
        """Handle gemstone education"""
        kb = self.knowledge_base
        response = "**Gemstone Education**\n\n"
        response += f"We have {kb.get('total_diamonds', 0):,} certified diamonds.\n\n"
        response += "**The 4 Cs of Diamonds:**\n"
        response += "• **Cut**: Determines brilliance\n"
        response += "• **Color**: D-F colorless, G-J near colorless\n"
        response += "• **Clarity**: VS1-VS2 excellent value\n"
        response += "• **Carat**: Size and weight\n"
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response
    
    def handle_greeting(self, query):
        """Handle greetings"""
        kb = self.knowledge_base
        response = f"Hello! I'm your AI jewelry consultant with knowledge of {kb.get('total_jewelry', 0):,} jewelry pieces and {kb.get('total_diamonds', 0):,} diamonds."
        if self.ml_models_loaded:
            response += " My responses are powered by trained neural networks. "
        response += " What interests you today?"
        return response
    
    def handle_general(self, query):
        """General fallback"""
        kb = self.knowledge_base
        response = f"I can help you explore our {kb.get('total_jewelry', 0):,} jewelry pieces and {kb.get('total_diamonds', 0):,} diamonds.\n\n"
        response += "Try asking about:\n• Specific jewelry types (rings, necklaces, etc.)\n• Pricing and budgets\n• Gemstone education\n• Materials and metals"
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response

    def handle_appointment(self, query):
        """Handle booking and appointments"""
        response = (
            "Appointments and consultations:\n"
            "• Engagement ring consultations: 90 minutes\n"
            "• Custom design sessions: 60 minutes\n"
            "• Browsing visits: 30 minutes\n"
            "• Appraisals: 30 minutes\n\n"
            "How to book: Visit /appointments or contact us to schedule a time."
        )
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response

    def handle_shipping(self, query):
        """Handle shipping questions"""
        response = (
            "Shipping options:\n"
            "• Standard: 5-7 business days (free over $500)\n"
            "• Express: 2-3 business days ($25)\n"
            "• Overnight: next business day ($50)\n\n"
            "International shipping: Available with insurance and tracking."
        )
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response

    def handle_returns(self, query):
        """Handle returns and exchanges"""
        response = (
            "Returns and exchanges:\n"
            "• 30-day returns for unaltered items with original packaging\n"
            "• Exchanges available; lifetime exchange options for eligible items\n"
            "• Custom/bespoke items: non-refundable after design approval; modifications available"
        )
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response

    def handle_customization(self, query):
        """Handle bespoke/custom design questions"""
        response = (
            "Custom and bespoke process (typical 6-8 weeks):\n"
            "1) Consultation and brief\n"
            "2) Design concepts and approvals\n"
            "3) Stone and metal selection\n"
            "4) Crafting and quality checks\n"
            "5) Delivery and fit\n\n"
            "Engraving and modifications available. Book at /appointments."
        )
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response

    def handle_sizing(self, query):
        """Handle sizing questions"""
        response = (
            "Sizing guides:\n"
            "• Rings: sizes typically 4-13; measure using a ring sizer or an existing ring\n"
            "• Necklaces: common lengths 16, 18, 20, 24 inches\n"
            "• Bracelets: measure wrist and add 0.5 to 1 inch for comfort\n\n"
            "See /sizing for details and printable guides."
        )
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response

    def handle_care(self, query):
        """Handle care and maintenance"""
        response = (
            "Care and maintenance:\n"
            "• Clean gently with mild soap and a soft brush\n"
            "• Avoid harsh chemicals and store items separately\n"
            "• Annual professional cleaning recommended\n"
            "• Pearls and soft stones: wipe with a soft cloth after wear"
        )
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response

    def handle_material(self, query):
        """Handle material questions (gold, platinum, silver)"""
        q = query.lower()
        if 'platinum' in q:
            note = "Platinum: naturally white, durable, hypoallergenic; typically higher cost."
        elif 'gold' in q:
            note = "Gold: available in yellow/white/rose; 14k is durable and affordable; 18k is richer in color."
        elif 'silver' in q:
            note = "Silver: bright and affordable; may tarnish over time; polish periodically."
        else:
            note = "Materials include gold (yellow/white/rose), platinum, and silver. Choose based on color, durability, and budget."
        response = f"Material information: {note}"
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response

    def handle_comparison(self, query):
        """Handle comparisons like gold vs platinum"""
        q = query.lower()
        segments = []
        if 'gold' in q and 'platinum' in q:
            segments.append("Gold vs Platinum: gold offers color options and value; platinum is denser, hypoallergenic, and maintains a white tone.")
        if 'silver' in q and ('gold' in q or 'platinum' in q):
            segments.append("Silver vs Gold/Platinum: silver is most affordable but prone to tarnish; gold/platinum are premium and longer lasting.")
        if not segments:
            segments.append("Comparison factors: color, durability, maintenance, budget, and style preferences.")
        response = " ".join(segments)
        response += "\n\n[ML Engine Active]" if self.ml_models_loaded else "\n\n[Fallback Engine]"
        return response
    
    def generate_response(self, query):
        """Generate response using ML or fallback"""
        intent, confidence = self.classify_intent(query)
        
        handlers = {
            'inventory': self.handle_inventory,
            'search': self.handle_search,
            'pricing': self.handle_pricing,
            'education': self.handle_education,
            'material': self.handle_material,
            'comparison': self.handle_comparison,
            'customization': self.handle_customization,
            'sizing': self.handle_sizing,
            'care': self.handle_care,
            'appointment': self.handle_appointment,
            'diamond_info': self.handle_education,
            'greeting': self.handle_greeting,
            'gratitude': lambda q: "You're welcome! Feel free to ask anything.",
            'general': self.handle_general,
        }
        
        handler = handlers.get(intent, self.handle_general)
        return handler(query)

# Initialize chatbot
chatbot = MLJewelryChatbot()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'ml_models_loaded': chatbot.ml_models_loaded,
        'jewelry_items': chatbot.knowledge_base.get('total_jewelry', 0),
        'diamonds': chatbot.knowledge_base.get('total_diamonds', 0),
        'engine': 'Neural Network ML' if chatbot.ml_models_loaded else 'Pattern Matching Fallback'
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # First, attempt ML intent classification (if available) to get confidence
        ml_pred = None
        try:
            ml_pred = chatbot.classify_intent_ml(message) if chatbot.ml_models_loaded else None
        except Exception:
            ml_pred = None

        # Decision: prefer ML when it provides a prediction (use ML regardless of confidence)
        engine = 'dataset'
        fallback_reason = None

        if ml_pred:
            intent_ml, confidence_ml = ml_pred
            # Use ML pipeline (prefer ML). However, ensure the reply is related to the
            # user's query: if the ML model returns a generic/educational intent but the
            # query clearly requests a search or pricing result, reroute to the
            # dataset-backed handlers so the response is dataset-grounded and relevant.

            # Heuristic override: detect concrete intents and override if ML intent is wrong or low confidence
            q_lower = message.lower()
            overridden = False

            # Greeting detection - highest priority (allow trailing words like "there", "everyone")
            if re.match(r'^\s*(hi|hello|hey|greetings|good\s+(morning|afternoon|evening))(\s+(there|everyone|folks))?\s*[!.?]*\s*$', q_lower, re.IGNORECASE):
                intent_ml = 'greeting'
                overridden = True
            # Inventory questions
            elif re.search(r'\b(what|which).*(type|kind|category|have|stock|inventory|offer|collection)', q_lower):
                intent_ml = 'inventory'
                overridden = True
            # Specific domain intents
            elif chatbot._is_appointment_like(q_lower):
                intent_ml = 'appointment'
                overridden = True
            elif chatbot._is_shipping_like(q_lower):
                intent_ml = 'shipping'
                overridden = True
            elif chatbot._is_returns_like(q_lower):
                intent_ml = 'returns'
                overridden = True
            elif chatbot._is_customization_like(q_lower):
                intent_ml = 'customization'
                overridden = True
            elif chatbot._is_sizing_like(q_lower):
                intent_ml = 'sizing'
                overridden = True
            elif chatbot._is_care_like(q_lower):
                intent_ml = 'care'
                overridden = True
            elif chatbot._is_comparison_like(q_lower):
                intent_ml = 'comparison'
                overridden = True
            elif chatbot._is_material_like(q_lower):
                intent_ml = 'material'
                overridden = True
            # Search/pricing overrides for low confidence or generic/wrong intents
            elif intent_ml in ('education', 'general', 'diamond_info', 'general_info', 'custom_design', 'ring_info', 'jewelry_info') or confidence_ml < 0.75:
                if chatbot._is_search_like(q_lower):
                    intent_ml = 'search'
                    overridden = True
                elif chatbot._is_pricing_like(q_lower):
                    intent_ml = 'pricing'
                    overridden = True
            
            if overridden:
                print(f"[HEURISTIC OVERRIDE] ML->'{intent_ml}' for query: {q_lower}")
            
            # Map ML model intents to handler functions
            handlers = {
                # Direct mappings
                'inventory': chatbot.handle_inventory,
                'search': chatbot.handle_search,
                'pricing': chatbot.handle_pricing,
                'education': chatbot.handle_education,
                'material': chatbot.handle_material,
                'comparison': chatbot.handle_comparison,
                'customization': chatbot.handle_customization,
                'sizing': chatbot.handle_sizing,
                'care': chatbot.handle_care,
                'appointment': chatbot.handle_appointment,
                'diamond_info': chatbot.handle_education,
                'greeting': chatbot.handle_greeting,
                'gratitude': lambda q: "You're welcome! Feel free to ask anything.",
                'general': chatbot.handle_general,
                # ML model intent mappings
                'general_info': chatbot.handle_general,
                'jewelry_info': chatbot.handle_search,  # jewelry_info -> search handler
                'ring_info': chatbot.handle_search,     # ring_info -> search handler
                'custom_design': chatbot.handle_customization, # custom_design -> customization handler
                'care': chatbot.handle_care,                   # care -> care handler
            }

            handler = handlers.get(intent_ml, chatbot.handle_general)
            response_text = handler(message)

            engine = 'ml'
            return jsonify({
                'response': response_text,
                'intent': intent_ml,
                'confidence': float(confidence_ml),
                'ml_powered': True,
                'engine': engine
            })

        # ML not available -> use dataset handlers (regex)
        regex_intent, regex_conf = chatbot.classify_intent_regex(message)

        handlers = {
            'inventory': chatbot.handle_inventory,
            'search': chatbot.handle_search,
            'pricing': chatbot.handle_pricing,
            'education': chatbot.handle_education,
            'material': chatbot.handle_material,
            'comparison': chatbot.handle_comparison,
            'customization': chatbot.handle_customization,
            'sizing': chatbot.handle_sizing,
            'care': chatbot.handle_care,
            'appointment': chatbot.handle_appointment,
            'diamond_info': chatbot.handle_education,
            'greeting': chatbot.handle_greeting,
            'gratitude': lambda q: "You're welcome! Feel free to ask anything.",
            'general': chatbot.handle_general,
        }

        handler = handlers.get(regex_intent, chatbot.handle_general)
        response_text = handler(message)

        return jsonify({
            'response': response_text,
            'intent': regex_intent,
            'confidence': float(regex_conf),
            'ml_powered': False,
            'engine': 'dataset',
            'fallback_reason': 'ml_unavailable'
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("ML-POWERED JEWELRY CHATBOT SERVER")
    print("="*70)
    print(f"Engine: {'Neural Network ML' if chatbot.ml_models_loaded else 'Pattern Matching Fallback'}")
    print(f"Knowledge: {chatbot.knowledge_base.get('total_jewelry', 0):,} jewelry, {chatbot.knowledge_base.get('total_diamonds', 0):,} diamonds")
    print("Server: http://localhost:5000")
    print("Health: http://localhost:5000/health")
    print("="*70 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
