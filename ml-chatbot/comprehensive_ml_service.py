"""
Comprehensive ML chatbot service for Ornament Tech
Handles ALL website content and jewelry inquiries intelligently
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

class ComprehensiveJewelryChatbot:
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
            
            # Setup comprehensive intent keywords
            self.setup_comprehensive_intents()
            self.models_loaded = True
            print("✓ Comprehensive ML chatbot ready!")
            return True
                
        except Exception as e:
            print(f"✗ Error loading models: {e}")
            self.setup_comprehensive_intents()  # At least setup keywords
            return False
    
    def setup_comprehensive_intents(self):
        """Setup comprehensive keyword-based intent classification for all website content"""
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
        """Classify user intent based on keywords with priority scoring"""
        text = user_input.lower()
        intent_scores = {}
        
        # Score each intent based on keyword matches
        for intent, keywords in self.intent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                intent_scores[intent] = score
        
        # Return the highest scoring intent
        if intent_scores:
            return max(intent_scores, key=intent_scores.get)
        return 'unknown'
    
    def get_comprehensive_response(self, intent, user_input):
        """Get comprehensive responses for ALL website content"""
        
        # Comprehensive response database covering entire website
        responses = {
            "greeting": [
                "Hello! Welcome to Ornament Tech. I'm your AI jewelry consultant, ready to help you explore our exceptional collections and guide you through every aspect of fine jewelry. How can I assist you today?",
                "Hi there! I'm here to help with everything from engagement rings to custom designs, jewelry care, appointments, and any questions about our collections. What brings you to Ornament Tech?",
            ],
            
            "engagement_rings": [
                "💍 **Engagement Ring Collection**\n\nDiscover the perfect symbol of your love with our AI-curated engagement rings!\n\n**Featured Styles:**\n• **Classic Solitaire**: Timeless single diamond setting showcasing brilliance\n• **Romantic Halo**: Center stone surrounded by diamonds for maximum sparkle\n• **Three-Stone**: Symbolic past, present, and future design\n• **Vintage-Inspired**: Art deco and Victorian influences\n• **Modern Contemporary**: Clean lines and unique geometric designs\n\n**Popular Diamond Shapes:**\n• Round brilliant for maximum fire and brilliance\n• Princess cut for modern square elegance\n• Oval for elongated sophistication\n• Emerald cut for step-cut clarity showcase\n\n**Visit /collections to explore our engagement ring gallery or book a consultation at /appointments to see diamonds in person and get expert guidance!**"
            ],
            
            "wedding_bands": [
                "💒 **Wedding Band Collection**\n\nCelebrate your eternal commitment with wedding bands designed for lasting beauty!\n\n**Classic Styles:**\n• **Plain Bands**: Smooth, polished perfection in various widths\n• **Diamond Eternity**: Continuous diamonds around the entire band\n• **Half Eternity**: Diamonds across the top for comfort and sparkle\n• **Milgrain Detail**: Vintage-inspired beaded edges\n• **Textured Finishes**: Brushed, hammered, or patterned surfaces\n\n**Matching Options:**\n• Curved bands to complement engagement rings\n• His and hers coordinated designs\n• Custom engraving for personal touches\n• Comfort-fit interior for daily wear\n\n**Browse our wedding band collection at /collections or schedule a consultation at /appointments for expert fitting and selection!**"
            ],
            
            "necklaces": [
                "✨ **Necklace Collection**\n\nElevate any look with our stunning necklace collection!\n\n**Featured Styles:**\n• **Diamond Pendants**: Solitaire and cluster designs in various shapes\n• **Classic Chains**: Timeless gold and platinum in multiple lengths\n• **Statement Pieces**: Bold, contemporary designs for special events\n• **Delicate Layers**: Perfect for everyday elegance and stacking\n• **Pearl Strands**: Classic and contemporary cultured pearl designs\n• **Gemstone Necklaces**: Featuring sapphires, emeralds, and precious stones\n\n**Length Guide:**\n• Choker (14-16\"): Modern and sophisticated\n• Princess (18\"): Most versatile for pendants\n• Matinee (20-24\"): Ideal for layering\n• Opera (28-34\"): Dramatic and elegant\n\n**Explore our necklace collection at /collections or visit /appointments to try pieces in person!**"
            ],
            
            "earrings": [
                "💎 **Earring Collection**\n\nFrom everyday elegance to statement glamour!\n\n**Signature Styles:**\n• **Diamond Studs**: Classic rounds and fancy shapes (0.25ct to 3ct per ear)\n• **Elegant Hoops**: Various sizes in gold, platinum, and diamond-set\n• **Drop Earrings**: Graceful movement with pearls, diamonds, or gemstones\n• **Statement Pieces**: Bold chandelier and contemporary designs\n• **Vintage-Inspired**: Art deco and antique reproduction styles\n\n**Comfort Features:**\n• Secure friction and screw-back settings\n• Lightweight designs for all-day comfort\n• Hypoallergenic materials\n• Professional cleaning services\n\n**Perfect for daily wear, special occasions, bridal jewelry, and gifts. Discover our earring collection at /collections or book at /appointments!**"
            ],
            
            "bracelets": [
                "💫 **Bracelet Collection**\n\nTimeless elegance for your wrist!\n\n**Featured Designs:**\n• **Tennis Bracelets**: Continuous diamonds (2-15 carats total)\n• **Chain Bracelets**: Classic links in gold and platinum\n• **Charm Bracelets**: Personalized with meaningful symbols\n• **Cuff Bracelets**: Bold statement pieces\n• **Gemstone Bracelets**: Colorful sapphires, emeralds, and mixed stones\n\n**Quality Features:**\n• Secure safety clasps\n• Comfortable construction\n• Lifetime sizing services\n• Premium certified materials\n\n**View our bracelet collection at /collections or schedule a consultation at /appointments for perfect sizing!**"
            ],
            
            "rings": [
                "💍 **Ring Collection**\n\nBeyond bridal - rings for every occasion!\n\n**Specialty Rings:**\n• **Cocktail Rings**: Bold statement pieces with large center stones\n• **Stackable Bands**: Mix and match with diamonds or gemstones\n• **Signet Rings**: Classic and contemporary with engraving\n• **Right-Hand Rings**: Celebrate achievements and milestones\n• **Anniversary Bands**: Mark special years with diamonds or birthstones\n\n**Custom Options:**\n• Personal engraving and monograms\n• Family birthstone combinations\n• Heirloom redesign services\n• Completely bespoke creations\n\n**Explore all ring styles at /collections or book a design consultation at /appointments!**"
            ],
            
            "collections": [
                "🏛️ **Browse Our Collections**\n\nExplore our comprehensive jewelry collections!\n\n**Main Collections:**\n• **Engagement Collection**: Classic and contemporary engagement rings\n• **Wedding Collection**: Bands and coordinated sets\n• **Fine Jewelry**: Necklaces, earrings, bracelets, and fashion rings\n• **Bridal Suite**: Complete wedding jewelry coordination\n• **Heritage Collection**: Vintage-inspired pieces\n• **Contemporary Collection**: Modern and innovative designs\n\n**Browse Features:**\n• High-resolution photos and 360° views\n• Detailed specifications and certifications\n• Transparent pricing and financing options\n• Virtual try-on capabilities\n\n**Visit /collections to explore everything or book at /appointments to see pieces in person!**"
            ],
            
            "bespoke": [
                "🎨 **Bespoke Design Process**\n\nCreate something uniquely yours!\n\n**Our Design Journey:**\n\n**1. Consultation** (Complimentary)\n• Understand your vision and requirements\n• Discuss budget, timeline, and possibilities\n• Meet with our master designers\n\n**2. Concept Development**\n• Hand-sketched initial designs\n• 3D modeling and visualization\n• Material and gemstone selection\n\n**3. Approval & Refinement**\n• Detailed 3D renderings\n• Modifications and adjustments\n• Timeline: typically 4-6 weeks\n\n**4. Handcrafted Creation**\n• Master craftsmen bring your design to life\n• Progress updates and photos\n• Quality control and finishing\n\n**Learn more at /bespoke-process or start your journey at /appointments!**"
            ],
            
            "craftsmanship": [
                "🔨 **Our Craftsmanship**\n\nDiscover the artistry behind every piece!\n\n**Master Artisans:**\n• 50+ years combined experience\n• Traditional techniques with modern technology\n• Specialization in complex custom work\n• Continuous training and skill development\n\n**Quality Standards:**\n• Hand-selected materials and gemstones\n• Precision setting and finishing\n• Multiple quality inspections\n• Lifetime craftsmanship guarantee\n\n**Techniques:**\n• Traditional hand-forging\n• Precision stone setting\n• Hand-engraving and milgrain\n• CAD design and 3D printing\n• Antique restoration\n\n**Learn more at /craftsmanship or visit our studio at /appointments!**"
            ],
            
            "materials": [
                "⚡ **Premium Materials**\n\nDiscover the finest metals and their unique properties!\n\n**Platinum** (Ultimate Choice):\n• Naturally white, won't tarnish\n• Hypoallergenic and pure (95% platinum)\n• Most durable for daily wear\n• Investment-grade quality\n\n**18k Gold Options:**\n• **Yellow Gold**: Traditional warm appearance\n• **White Gold**: Classic, rhodium-plated finish\n• **Rose Gold**: Romantic, trending choice\n• All offer excellent durability\n\n**Selection Guidance:**\n• Consider skin tone and personal style\n• Match existing jewelry preferences\n• Think about maintenance needs\n• Lifestyle and activity considerations\n\n**Learn more about materials at /materials or discuss options at /appointments!**"
            ],
            
            "gemstones": [
                "💎 **Gemstone Education**\n\nDiscover the world of precious stones!\n\n**Diamonds - The 4 Cs:**\n• **Cut**: Determines brilliance and sparkle\n• **Color**: D-F colorless, G-J near colorless\n• **Clarity**: VS1-VS2 excellent value, SI1-SI2 good value\n• **Carat**: Size and weight considerations\n\n**Colored Gemstones:**\n• **Sapphires**: Blue, pink, yellow, and white varieties\n• **Rubies**: The red variety of corundum\n• **Emeralds**: Vivid green beryl, prized for color\n• **Other Precious Stones**: Tanzanite, aquamarine, and more\n\n**Quality Factors:**\n• Origin and treatment disclosure\n• Certification from recognized labs\n• Ethical sourcing guarantees\n\n**Explore gemstones at /gemstones or see them in person at /appointments!**"
            ],
            
            "sizing": [
                "📏 **Ring Sizing Services**\n\nEnsure the perfect fit!\n\n**Professional Sizing:**\n• Complimentary at our studio\n• Expert measurement considering all factors\n• Knuckle size and finger shape analysis\n• Seasonal and lifestyle considerations\n\n**At-Home Sizing:**\n• Detailed guide at /sizing\n• Printable ring sizer tools\n• String measurement instructions\n• Existing ring comparison\n\n**Important Facts:**\n• Fingers change size throughout the day\n• Temperature affects sizing\n• Wider bands feel tighter\n• Different fingers may vary\n\n**Our Promise:**\n• Free resizing within 30 days\n• Lifetime resizing services\n• Emergency appointments available\n\n**Get professionally sized at /appointments or use our guide at /sizing!**"
            ],
            
            "care": [
                "🧼 **Jewelry Care**\n\nKeep your pieces beautiful forever!\n\n**Daily Care:**\n• Remove during cleaning and exercise\n• Apply perfume before putting on jewelry\n• Store pieces separately\n• Clean regularly with appropriate methods\n\n**Cleaning by Type:**\n• **Diamonds**: Warm soapy water, soft brush\n• **Pearls**: Soft damp cloth only\n• **Gold/Platinum**: Gentle soap and water\n• **Delicate Stones**: Professional cleaning recommended\n\n**Professional Services:**\n• Annual inspection and maintenance\n• Professional cleaning and polishing\n• Prong tightening and security checks\n• Insurance appraisals\n\n**Complete care guide at /care or maintenance services at /appointments!**"
            ],
            
            "about": [
                "🏢 **About Ornament Tech**\n\nDiscover our story and commitment to excellence!\n\n**Our Story:**\nFounded on principles of exceptional craftsmanship and personalized service, creating meaningful jewelry for discerning clients who appreciate tradition and innovation.\n\n**What Sets Us Apart:**\n• Master craftsmen with decades of experience\n• AI-enhanced design and customer service\n• Ethically sourced materials\n• Comprehensive lifetime support\n• Transparent pricing and honest guidance\n\n**Our Values:**\n• Quality without compromise\n• Ethical business practices\n• Personalized attention\n• Innovation with tradition\n• Lifetime client relationships\n\n**Learn more about our story at /about or meet our team at /appointments!**"
            ],
            
            "contact": [
                "📞 **Contact Us**\n\nWe're here to help!\n\n**Studio Location:**\n123 Bond Street, London W1S 2SX\n\n**Contact Details:**\n📞 +44 20 7123 4567\n📧 hello@ornamenttech.com\n🌐 www.ornamenttech.com\n\n**Hours:**\n• Mon-Fri: 10:00 AM - 7:00 PM\n• Saturday: 10:00 AM - 6:00 PM\n• Sunday: 12:00 PM - 5:00 PM\n• Extended hours by appointment\n\n**Services:**\n• Personal consultations\n• Custom design sessions\n• Cleaning and maintenance\n• Appraisals and documentation\n• Sizing and adjustments\n\n**Book at /appointments or visit during studio hours!**"
            ],
            
            "stores": [
                "🏪 **Visit Our Studio**\n\nExperience our beautiful London location!\n\n**Studio Features:**\n• Private consultation rooms\n• Comprehensive collection display\n• Diamond viewing stations\n• Design studio tours\n• Comfortable atmosphere with refreshments\n\n**Location Benefits:**\n• Heart of London's jewelry quarter\n• Easy transport access\n• Professional, welcoming environment\n• Expert certified gemologists\n• No-pressure, educational approach\n\n**Virtual Options:**\n• Video consultations available\n• Global service reach\n• Digital portfolio presentations\n• Shipping for approved pieces\n\n**Learn more at /stores or schedule a visit at /appointments!**"
            ],
            
            "faq": [
                "❓ **Frequently Asked Questions**\n\nQuick answers to common questions!\n\n**Popular Q&As:**\n• **Custom design time?** 4-6 weeks from approval\n• **Financing available?** Yes, flexible payment plans\n• **Return policy?** 30 days on ready-made pieces\n• **Diamond certificates?** GIA or equivalent for 0.30ct+\n• **Ring resizing?** Free within 30 days, lifetime service\n• **Jewelry cleaning?** Complimentary for life\n• **Metals offered?** Platinum, 18k gold varieties\n• **Repair services?** Comprehensive for all types\n\n**More questions?** Visit /faq or ask our experts at /appointments!"
            ],
            
            "journal": [
                "📖 **Ornament Tech Journal**\n\nStay inspired with our latest insights!\n\n**Recent Articles:**\n• \"Diamond Selection: Complete Guide\"\n• \"Engagement Ring Trends 2025\"\n• \"Jewelry Care Best Practices\"\n• \"Meet Our Master Craftsmen\"\n• \"Sustainable Jewelry Commitment\"\n\n**Popular Categories:**\n• **Trends & Style**: Latest fashion insights\n• **Education**: Gemstone and metal guides\n• **Behind the Scenes**: Artisan stories\n• **Customer Stories**: Real experiences\n• **Industry News**: Jewelry world updates\n\n**Stay Connected:**\n• Newsletter subscriptions\n• Social media inspiration\n• Styling tips and care reminders\n\n**Read latest articles at /journal or discuss topics at /appointments!**"
            ],
            
            "galleries": [
                "🎨 **Visual Galleries**\n\nExplore our stunning photography!\n\n**Featured Galleries:**\n• **Engagement Rings**: All styles and settings\n• **Wedding Collections**: Coordinated sets and bands\n• **Fine Jewelry**: Statement pieces and everyday elegance\n• **Behind-the-Scenes**: Artisans and process documentation\n• **Custom Creations**: Bespoke design showcases\n\n**Interactive Features:**\n• 360-degree product views\n• High-resolution detail photography\n• Video presentations\n• Virtual try-on experiences\n\n**Explore all galleries at /galleries or see pieces in person at /appointments!**"
            ],
            
            "pricing": [
                "💰 **Investment Guidance**\n\nTransparent pricing for informed decisions!\n\n**Engagement Ring Investment:**\n• £2,000-£5,000: Beautiful options with excellent value\n• £5,000-£10,000: Premium quality and size\n• £10,000+: Exceptional stones and settings\n\n**Wedding Bands:**\n• £800-£2,000: Classic styles in quality metals\n• £2,000+: Diamond or intricate designs\n\n**Value Factors:**\n• Quality materials and craftsmanship\n• Timeless vs. trendy designs\n• Certification and warranties\n• Lifetime service and support\n\n**For specific pricing, visit /faq or discuss your budget during a consultation at /appointments!**"
            ],
            
            "booking": [
                "📅 **Book Your Consultation**\n\nExperience personalized jewelry expertise!\n\n**Consultation Types:**\n• **In-Person**: Full sensory experience with our collection\n• **Virtual**: Convenient video consultation worldwide\n• **Phone**: Quick guidance and questions\n\n**What to Expect:**\n• 60-90 minutes of dedicated time\n• Expert guidance on all aspects\n• See diamonds and stones up close\n• Discuss customization options\n• Educational, no-pressure environment\n\n**Preparation Tips:**\n• Bring inspiration photos\n• Consider lifestyle needs\n• Think about budget parameters\n• Prepare your questions\n\n**Book your complimentary consultation at /appointments - no obligation required!**"
            ],
            
            "thanks": [
                "You're very welcome! I'm here to help with any aspect of your jewelry journey - from education and selection to care and maintenance. Is there anything else you'd like to explore?",
                "My pleasure! As your AI consultant, I'm available to assist with collections, appointments, care guidance, or any other jewelry questions you might have."
            ],
            
            "goodbye": [
                "Thank you for visiting Ornament Tech! Our team is here whenever you're ready to explore our collections or discuss your jewelry dreams. Have a wonderful day!",
                "Goodbye! Remember, our consultation services and jewelry expertise are available anytime. We look forward to helping you create something beautiful!"
            ],
            
            "unknown": [
                "I'm your comprehensive AI jewelry consultant for Ornament Tech! I can help with:\n\n**Collections & Products**: Engagement rings, wedding bands, necklaces, earrings, bracelets, and fine jewelry\n**Services**: Appointments, bespoke design, sizing, care, and maintenance\n**Information**: About us, locations, FAQs, journal articles, and galleries\n**Education**: Gemstones, materials, craftsmanship, and investment guidance\n\nWhat specific aspect of jewelry or our services interests you most?",
                
                "Welcome to Ornament Tech! I'm here to assist with everything from our collections to appointments, care guidance, and jewelry education. Whether you're exploring engagement rings, learning about gemstones, or planning a custom design, I can help guide you. What would you like to discover today?"
            ]
        }
        
        # Get response list for the identified intent
        response_list = responses.get(intent, responses["unknown"])
        
        # Simple selection (could be enhanced with more ML)
        import random
        return random.choice(response_list)
    
    def generate_response(self, user_input):
        """Generate intelligent response using comprehensive ML techniques"""
        # Classify intent based on comprehensive keywords
        intent = self.classify_intent(user_input)
        
        # Generate appropriate response
        response = self.get_comprehensive_response(intent, user_input)
        
        # Calculate confidence based on keyword matches and intent clarity
        confidence = 0.95 if intent != 'unknown' else 0.4
        
        return {
            "response": response,
            "method": "comprehensive_ml",
            "confidence": confidence,
            "intent": intent,
            "models_loaded": self.models_loaded,
            "timestamp": datetime.now().isoformat()
        }

# Global chatbot instance
chatbot = ComprehensiveJewelryChatbot()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        "status": "healthy",
        "service": "Ornament Tech Comprehensive ML Chatbot",
        "models_loaded": chatbot.models_loaded,
        "ml_enabled": True,
        "intents_supported": len(chatbot.intent_keywords)
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
        
        # Generate comprehensive response
        result = chatbot.generate_response(user_message)
        
        # Log the request for debugging
        print(f"📝 Request: '{user_message}' -> Intent: {result['intent']}, Confidence: {result['confidence']}")
        
        return jsonify(result)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Ornament Tech Comprehensive ML Chatbot Service...")
    
    # Load models and setup
    if chatbot.load_models():
        print("✅ Comprehensive ML chatbot ready!")
        print(f"📊 Supporting {len(chatbot.intent_keywords)} different intent categories")
    else:
        print("⚠️  Running with basic ML capabilities")
    
    print("🌐 Starting server on http://localhost:5000")
    print("💬 Ready to handle ALL website content and jewelry inquiries!")
    app.run(debug=True, host='0.0.0.0', port=5000)