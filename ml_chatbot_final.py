"""
FINAL PRODUCTION ML CHATBOT - Fresh Implementation
Loads datasets, understands queries, provides intelligent responses
Run this standalone: python ml_chatbot_final.py
"""

import pandas as pd
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Ensure stdout can handle Unicode on Windows; if not, fall back silently
try:
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore[attr-defined]
except Exception:
    pass

app = Flask(__name__)
CORS(app)

class JewelryMLChatbot:
    def __init__(self):
        self.jewelry_data = None
        self.diamonds_data = None
        self.knowledge_base = {}
        print("Initializing ML Chatbot...")
        self.load_datasets()
        self.build_knowledge()
        print("ML Chatbot ready!")
    
    def load_datasets(self):
        """Load jewelry and diamond datasets"""
        try:
            # Try multiple possible locations
            paths = [
                'ml-chatbot/models/jewelry_dataset.csv',
                'jewelry_dataset.csv',
                'models/jewelry_dataset.csv'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    self.jewelry_data = pd.read_csv(path)
                    print(f"Loaded {len(self.jewelry_data)} jewelry items from {path}")
                    break
            
            paths = [
                'ml-chatbot/models/diamonds_dataset.csv',
                'diamonds_dataset.csv',
                'models/diamonds_dataset.csv'
            ]
            
            for path in paths:
                if os.path.exists(path):
                    self.diamonds_data = pd.read_csv(path)
                    print(f"Loaded {len(self.diamonds_data)} diamonds from {path}")
                    break
                    
            if self.jewelry_data is None:
                print("WARNING: Could not load jewelry dataset")
            if self.diamonds_data is None:
                print("WARNING: Could not load diamonds dataset")
                
        except Exception as e:
            print(f"ERROR loading datasets: {e}")
    
    def build_knowledge(self):
        """Build knowledge base from datasets"""
        if self.jewelry_data is not None:
            self.knowledge_base['categories'] = self.jewelry_data['category'].unique().tolist() if 'category' in self.jewelry_data.columns else []
            self.knowledge_base['materials'] = self.jewelry_data['metal'].unique().tolist() if 'metal' in self.jewelry_data.columns else []
            self.knowledge_base['stones'] = self.jewelry_data['stone'].unique().tolist() if 'stone' in self.jewelry_data.columns else []
            self.knowledge_base['total_jewelry'] = len(self.jewelry_data)
            
            # Calculate price ranges
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
        
        if self.jewelry_data is not None and self.diamonds_data is not None:
            print(f"Knowledge Base: {len(self.jewelry_data)} jewelry, {len(self.diamonds_data)} diamonds")
    
    def classify_intent(self, query):
        """Classify user intent using advanced pattern matching"""
        q = query.lower()
        
        # Inventory queries
        if re.search(r'(what|which|tell me|show me).*(type|kind|category|categories|collection|have|available|stock|inventory|sell|offer)', q):
            return 'inventory'
        
        # Product search (enhanced)
        if re.search(r'(show|find|search|looking for|want|need|interested in|browse).*(ring|necklace|earring|bracelet|jewelry|jewellery|pendant|chain)', q):
            return 'search'
        
        # Price queries (enhanced)
        if re.search(r'(price|cost|expensive|cheap|budget|afford|how much|value|worth|range)', q):
            return 'pricing'
        
        # Gemstone education (enhanced)
        if re.search(r'(diamond|ruby|emerald|sapphire|gemstone|stone|crystal).*(what|how|tell|explain|quality|grade|clarity|cut|carat)', q):
            return 'education'
        
        # Material queries (enhanced)
        if re.search(r'(gold|silver|platinum|metal|material|titanium|brass|copper|alloy)', q):
            return 'material'
        
        # Comparison (enhanced)
        if re.search(r'(compare|comparison|difference|differ|better|best|versus|vs|between|which one|should i)', q):
            return 'comparison'
        
        # Customization/Bespoke
        if re.search(r'(custom|customize|bespoke|design|personalize|engrave|make|create|unique)', q):
            return 'customization'
        
        # Sizing/Fit
        if re.search(r'(size|sizing|fit|fitting|measure|measurement|resize)', q):
            return 'sizing'
        
        # Care/Maintenance
        if re.search(r'(care|clean|maintain|polish|repair|fix|damage|warranty)', q):
            return 'care'
        
        # Appointment/Visit
        if re.search(r'(appointment|visit|store|location|book|schedule|meet|consultation)', q):
            return 'appointment'
        
        # Shipping/Delivery
        if re.search(r'(ship|shipping|deliver|delivery|send|courier|track|arrival)', q):
            return 'shipping'
        
        # Returns/Exchange
        if re.search(r'(return|exchange|refund|money back|policy|replace)', q):
            return 'returns'
        
        # Greeting
        if re.search(r'^(hi|hello|hey|good morning|good afternoon|good evening|greetings)', q):
            return 'greeting'
        
        # Gratitude
        if re.search(r'(thank|thanks|appreciate|grateful)', q):
            return 'gratitude'
        
        # Default - try to extract jewelry-related keywords
        if any(word in q for word in ['ring', 'necklace', 'earring', 'bracelet', 'jewelry', 'jewellery', 'diamond', 'gold', 'silver']):
            return 'search'  # Treat as search if jewelry-related
        
        return 'general'
    
    def handle_inventory(self, query):
        """Answer inventory questions with real data"""
        kb = self.knowledge_base
        
        response = f"✨ **Our Complete Jewelry Collection**\n\n"
        response += f"📊 **Total Items:** {kb.get('total_jewelry', 0):,} jewelry pieces\n\n"
        
        # Categories
        if kb.get('categories'):
            response += "**Jewelry Categories:**\n"
            for cat in kb['categories'][:10]:
                if self.jewelry_data is not None:
                    count = len(self.jewelry_data[self.jewelry_data['category'] == cat])
                    response += f"• {cat.capitalize()}: {count:,} pieces\n"
        
        # Materials
        if kb.get('materials'):
            response += "\n**Premium Materials:**\n"
            for mat in kb['materials'][:8]:
                if self.jewelry_data is not None and mat and str(mat) != 'nan':
                    count = len(self.jewelry_data[self.jewelry_data['metal'] == mat])
                    response += f"• {mat}: {count:,} pieces\n"
        
        # Gemstones
        if kb.get('stones'):
            response += "\n**Gemstones Available:**\n"
            stones = [s for s in kb['stones'] if s and str(s).lower() not in ['none', 'nan']][:8]
            for stone in stones:
                if self.jewelry_data is not None:
                    count = len(self.jewelry_data[self.jewelry_data['stone'] == stone])
                    response += f"• {stone}: {count:,} pieces\n"
        
        # Pricing
        if kb.get('price_min'):
            response += f"\n**Price Range:** ${kb['price_min']:,.0f} - ${kb['price_max']:,.0f}\n"
            response += f"**Average Price:** ${kb['price_avg']:,.0f}\n"
        
        response += "\n💎 We also have {0:,} certified diamonds in our collection!".format(kb.get('total_diamonds', 0))
        
        return response
    
    def handle_search(self, query):
        """Handle product search queries"""
        q = query.lower()
        
        if self.jewelry_data is None:
            return "I apologize, but I'm currently unable to access our inventory. Please visit /collections to browse our pieces."
        
        # Extract search terms
        categories = ['ring', 'necklace', 'earring', 'bracelet', 'pendant']
        materials = ['gold', 'silver', 'platinum']
        stones = ['diamond', 'ruby', 'emerald', 'sapphire']
        
        results = self.jewelry_data.copy()
        filters_applied = []
        
        # Filter by category
        for cat in categories:
            if cat in q:
                results = results[results['category'].str.contains(cat, case=False, na=False)]
                filters_applied.append(f"category: {cat}")
        
        # Filter by material
        for mat in materials:
            if mat in q:
                results = results[results['metal'].str.contains(mat, case=False, na=False)]
                filters_applied.append(f"material: {mat}")
        
        # Filter by stone
        for stone in stones:
            if stone in q:
                results = results[results['stone'].str.contains(stone, case=False, na=False)]
                filters_applied.append(f"gemstone: {stone}")
        
        if len(results) == 0:
            return f"I couldn't find exact matches for your search. We have {len(self.jewelry_data):,} pieces in our collection. Try browsing by category at /collections!"
        
        # Build response
        response = f"🔍 **Found {len(results):,} pieces"
        if filters_applied:
            response += f" matching: {', '.join(filters_applied)}"
        response += "**\n\n"
        
        # Show top 5 results
        top_results = results.head(5)
        for idx, item in top_results.iterrows():
            response += f"• {item.get('category', 'Jewelry').capitalize()}"
            if 'metal' in item and pd.notna(item['metal']):
                response += f" - {item['metal']}"
            if 'stone' in item and pd.notna(item['stone']) and str(item['stone']).lower() != 'none':
                response += f" with {item['stone']}"
            if 'price' in item and pd.notna(item['price']):
                response += f" - ${item['price']:,.0f}"
            response += "\n"
        
        response += f"\n📍 Visit /collections to see all {len(results):,} matching pieces!"
        
        return response
    
    def handle_pricing(self, query):
        """Handle price-related queries"""
        if self.jewelry_data is None:
            return "I apologize, but I'm currently unable to access pricing information."
        
        kb = self.knowledge_base
        response = "💰 **Pricing Information**\n\n"
        response += f"**Price Range:** ${kb.get('price_min', 0):,.0f} - ${kb.get('price_max', 0):,.0f}\n"
        response += f"**Average Price:** ${kb.get('price_avg', 0):,.0f}\n\n"
        
        # Price categories
        if 'price' in self.jewelry_data.columns:
            under_1k = len(self.jewelry_data[self.jewelry_data['price'] < 1000])
            range_1k_5k = len(self.jewelry_data[(self.jewelry_data['price'] >= 1000) & (self.jewelry_data['price'] < 5000)])
            range_5k_10k = len(self.jewelry_data[(self.jewelry_data['price'] >= 5000) & (self.jewelry_data['price'] < 10000)])
            over_10k = len(self.jewelry_data[self.jewelry_data['price'] >= 10000])
            
            response += "**By Price Range:**\n"
            response += f"• Under $1,000: {under_1k:,} pieces\n"
            response += f"• $1,000 - $5,000: {range_1k_5k:,} pieces\n"
            response += f"• $5,000 - $10,000: {range_5k_10k:,} pieces\n"
            response += f"• Over $10,000: {over_10k:,} pieces\n"
        
        return response
    
    def handle_education(self, query):
        """Handle gemstone education queries"""
        response = "💎 **Gemstone Education**\n\n"
        
        if self.diamonds_data is not None:
            kb = self.knowledge_base
            response += f"We have {kb.get('total_diamonds', 0):,} certified diamonds in our collection.\n\n"
            
            if kb.get('diamond_cuts'):
                response += "**Available Cuts:** " + ", ".join(kb['diamond_cuts'][:5]) + "\n"
            if kb.get('diamond_colors'):
                response += "**Color Grades:** " + ", ".join(kb['diamond_colors'][:5]) + "\n\n"
        
        response += "**The 4 Cs of Diamonds:**\n"
        response += "• **Cut**: Determines brilliance and sparkle\n"
        response += "• **Color**: D-F colorless, G-J near colorless\n"
        response += "• **Clarity**: VS1-VS2 excellent value\n"
        response += "• **Carat**: Size and weight\n\n"
        response += "Visit /gemstones to learn more!"
        
        return response
    
    def handle_greeting(self, query):
        """Handle greeting queries"""
        kb = self.knowledge_base
        return f"Hello! 👋 I'm your AI jewelry consultant with knowledge of {kb.get('total_jewelry', 0):,} jewelry pieces and {kb.get('total_diamonds', 0):,} diamonds. I can help you find the perfect piece, explain gemstone quality, discuss pricing, or answer any questions about our collection. What interests you today?"
    
    def handle_comparison(self, query):
        """Handle comparison queries"""
        q = query.lower()
        
        if self.jewelry_data is None:
            return "I apologize, but I'm currently unable to access comparison data."
        
        # Try to extract what's being compared
        response = "🔍 **Jewelry Comparison**\n\n"
        
        # Look for specific items
        categories = ['ring', 'necklace', 'earring', 'bracelet']
        materials = ['gold', 'silver', 'platinum']
        stones = ['diamond', 'ruby', 'emerald', 'sapphire']
        
        found_cats = [cat for cat in categories if cat in q]
        found_mats = [mat for mat in materials if mat in q]
        found_stones = [stone for stone in stones if stone in q]
        
        if len(found_cats) >= 2:
            # Compare categories
            for cat in found_cats[:2]:
                count = len(self.jewelry_data[self.jewelry_data['category'].str.contains(cat, case=False, na=False)])
                avg_price = self.jewelry_data[self.jewelry_data['category'].str.contains(cat, case=False, na=False)]['price'].mean() if count > 0 else 0
                response += f"**{cat.capitalize()}s:** {count:,} pieces, avg ${avg_price:,.0f}\n"
        elif len(found_mats) >= 2:
            # Compare materials
            for mat in found_mats[:2]:
                count = len(self.jewelry_data[self.jewelry_data['metal'].str.contains(mat, case=False, na=False)])
                avg_price = self.jewelry_data[self.jewelry_data['metal'].str.contains(mat, case=False, na=False)]['price'].mean() if count > 0 else 0
                response += f"**{mat.capitalize()}:** {count:,} pieces, avg ${avg_price:,.0f}\n"
        else:
            response += "I can compare jewelry by category (rings vs necklaces), material (gold vs platinum), or gemstone. What would you like to compare?\n"
        
        response += "\n💡 All our pieces are crafted with premium materials and come with certification."
        return response
    
    def handle_material(self, query):
        """Handle material-related queries"""
        if self.jewelry_data is None:
            return "I apologize, but I'm currently unable to access material information."
        
        kb = self.knowledge_base
        q = query.lower()
        
        response = "⚜️ **Premium Materials**\n\n"
        
        # Check if asking about specific material
        materials_in_query = [mat for mat in ['gold', 'silver', 'platinum', 'titanium'] if mat in q]
        
        if materials_in_query:
            for mat in materials_in_query:
                items = self.jewelry_data[self.jewelry_data['metal'].str.contains(mat, case=False, na=False)]
                if len(items) > 0:
                    response += f"**{mat.capitalize()}:**\n"
                    response += f"• {len(items):,} pieces available\n"
                    response += f"• Price range: ${items['price'].min():,.0f} - ${items['price'].max():,.0f}\n"
                    response += f"• Average: ${items['price'].mean():,.0f}\n\n"
        else:
            # General material info
            if kb.get('materials'):
                response += "**Available Materials:**\n"
                for mat in kb['materials'][:10]:
                    if mat and str(mat) != 'nan':
                        count = len(self.jewelry_data[self.jewelry_data['metal'] == mat])
                        response += f"• {mat}: {count:,} pieces\n"
        
        response += "\n✨ All metals are ethically sourced and come with quality certification."
        return response
    
    def handle_customization(self, query):
        """Handle customization/bespoke queries"""
        return """🎨 **Bespoke Jewelry Design**

We offer complete customization services:

**Design Options:**
• Create from scratch with our master jewelers
• Modify existing designs to your preferences
• Engrave personal messages
• Choose your own gemstones and settings

**Process:**
1. **Consultation**: Discuss your vision (book at /appointments)
2. **Design**: Our team creates 3D renders
3. **Selection**: Choose materials and gemstones
4. **Crafting**: Master artisans bring it to life (2-6 weeks)
5. **Delivery**: Your unique piece with certification

**Popular Custom Requests:**
• Engagement rings with family heirlooms
• Anniversary pieces with birthstones
• Corporate gifts with logos
• Redesigning inherited jewelry

📍 Visit /bespoke-process to learn more or /appointments to schedule a consultation!"""
    
    def handle_sizing(self, query):
        """Handle sizing queries"""
        return """📏 **Jewelry Sizing Guide**

**Ring Sizing:**
• US sizes 4-13 available
• Free professional sizing with purchase
• Complimentary resize within 60 days
• How to measure at home guide at /sizing

**Necklace Lengths:**
• Choker: 14-16 inches
• Princess: 18 inches (most popular)
• Matinee: 20-24 inches
• Opera: 28-34 inches

**Bracelet Sizing:**
• Standard: 7-7.5 inches
• Adjustable options available
• Custom sizing upon request

**Need Help?**
• Visit /sizing for detailed measurement guides
• Book fitting appointment at /appointments
• Free adjustments on all purchases

💡 **Pro Tip**: Bring a ring that fits well to your appointment for accurate sizing!"""
    
    def handle_care(self, query):
        """Handle care and maintenance queries"""
        return """✨ **Jewelry Care & Maintenance**

**Daily Care:**
• Remove jewelry before swimming, exercising, or sleeping
• Apply perfume/lotion before putting on jewelry
• Store pieces separately to prevent scratching

**Cleaning:**
• **Gold/Platinum**: Warm water + mild soap, soft brush
• **Silver**: Polishing cloth, silver cleaner for tarnish
• **Diamonds**: Gentle scrub with soft toothbrush
• **Pearls/Opals**: Wipe with damp cloth only (no soap!)

**Professional Services:**
• Free cleaning and inspection every 6 months
• Professional polishing: $25-75
• Prong tightening: $30-50
• Rhodium plating (white gold): $75-150

**Warranty:**
• Lifetime warranty on manufacturing defects
• 1-year warranty on gemstone settings
• Free repairs within first year

📍 Visit /care for detailed guides or book a professional cleaning at /appointments!

🛡️ **Insurance**: We recommend insuring pieces over $2,000."""
    
    def handle_appointment(self, query):
        """Handle appointment queries"""
        kb = self.knowledge_base
        return f"""📅 **Book Your Personal Consultation**

**Why Visit Us:**
• View {kb.get('total_jewelry', 0):,} pieces in person
• Try on and compare different styles
• Expert guidance from certified gemologists
• Discuss custom design options
• Professional sizing and fitting

**Appointment Types:**
• **Engagement Ring Consultation** (90 min): Diamond education, setting selection
• **General Browse** (30 min): Explore our collection with guidance
• **Custom Design** (60 min): Bring your vision to life
• **Appraisal/Trade-in** (30 min): Get expert valuation

**Available Times:**
• Monday-Friday: 10 AM - 7 PM
• Saturday: 10 AM - 6 PM
• Sunday: 12 PM - 5 PM

**What to Expect:**
• Private viewing room
• Complimentary refreshments
• No pressure, expert advice
• Take your time deciding

📍 **Book Now:** Visit /appointments
📞 **Call:** Available on contact page
🏪 **Locations:** /stores

💎 Walk-ins welcome but appointments recommended for personalized service!"""
    
    def handle_shipping(self, query):
        """Handle shipping queries"""
        return """📦 **Shipping & Delivery**

**Domestic Shipping:**
• **Free Standard** (5-7 business days) on orders $100+
• **Express** (2-3 business days): $25
• **Overnight** (1 business day): $50

**International Shipping:**
• Available to 50+ countries
• Rates calculated at checkout
• Customs duties may apply (not included)
• Fully insured and tracked

**Security:**
• ✅ Signature required on all jewelry shipments
• ✅ Fully insured up to declared value
• ✅ Discreet packaging (no jewelry branding)
• ✅ Real-time tracking provided

**Custom/Bespoke Orders:**
• 2-6 weeks production time
• Priority shipping included
• Updates every week during creation

**Processing Time:**
• In-stock items: 1-2 business days
• Custom pieces: 2-6 weeks
• Rush service available (+$100)

📍 Track orders in your account or contact us for updates!"""
    
    def handle_returns(self, query):
        """Handle returns and exchange queries"""
        return """↩️ **Returns & Exchange Policy**

**30-Day Return Policy:**
• Full refund within 30 days of delivery
• Item must be unworn and in original condition
• All original packaging and certificates included
• Free return shipping provided

**Lifetime Exchange:**
• Exchange for store credit anytime
• Upgrade to higher value pieces
• Trade-in your old jewelry

**Custom/Bespoke Items:**
• Non-refundable (made to order)
• Modifications covered under warranty
• Quality guarantee - we'll make it right

**How to Return:**
1. Contact us within 30 days
2. Receive prepaid return label
3. Ship item with tracking
4. Refund processed within 5-7 days

**Exceptions:**
• Engraved items (custom order)
• Resized rings beyond standard
• Worn or damaged items

**Need Help?**
📍 Visit /faq for detailed policy
📧 Contact support on /contact
💬 Chat with me for specific questions

✨ **Our Promise**: If you're not 100% satisfied, we'll make it right!"""
    
    def handle_gratitude(self, query):
        """Handle thank you messages"""
        return "You're very welcome! 😊 I'm here whenever you need help with jewelry selection, gemstone education, pricing, or any other questions. Feel free to ask me anything, or visit /appointments to schedule a personal consultation with our experts!"
    
    def handle_general(self, query):
        """Handle general queries with intelligent fallback"""
        kb = self.knowledge_base
        q = query.lower()
        
        # Try to extract what they're asking about
        response = ""
        
        # Check if mentioning specific jewelry terms
        if any(word in q for word in ['engagement', 'wedding', 'bride', 'marry']):
            response = f"💍 **Engagement & Bridal Collection**\n\n"
            response += f"We have a stunning collection perfect for your special day!\n\n"
            if self.jewelry_data is not None:
                rings = self.jewelry_data[self.jewelry_data['category'].str.contains('ring', case=False, na=False)]
                response += f"• {len(rings):,} rings including engagement and wedding bands\n"
                response += f"• Price range: ${rings['price'].min():,.0f} - ${rings['price'].max():,.0f}\n\n"
            response += "💎 Visit /collections to explore or /appointments for a personal consultation!"
            return response
        
        # Default intelligent response
        response = f"🤖 **I'm Your AI Jewelry Consultant**\n\n"
        response += f"I have access to {kb.get('total_jewelry', 0):,} jewelry pieces and {kb.get('total_diamonds', 0):,} diamonds.\n\n"
        response += "**I can help you with:**\n"
        response += "• 🔍 Finding specific jewelry (rings, necklaces, etc.)\n"
        response += "• 💰 Pricing and budget guidance\n"
        response += "• 💎 Gemstone education and quality\n"
        response += "• ⚖️ Comparing different pieces\n"
        response += "• 🎨 Custom design options\n"
        response += "• 📏 Sizing and fitting\n"
        response += "• ✨ Care and maintenance tips\n\n"
        response += "**What would you like to know?**"
        
        return response
    
    def generate_response(self, query):
        """Generate intelligent response based on query"""
        intent = self.classify_intent(query)
        
        handlers = {
            'inventory': self.handle_inventory,
            'search': self.handle_search,
            'pricing': self.handle_pricing,
            'education': self.handle_education,
            'greeting': self.handle_greeting,
            'comparison': self.handle_comparison,
            'material': self.handle_material,
            'customization': self.handle_customization,
            'sizing': self.handle_sizing,
            'care': self.handle_care,
            'appointment': self.handle_appointment,
            'shipping': self.handle_shipping,
            'returns': self.handle_returns,
            'gratitude': self.handle_gratitude,
            'general': self.handle_general,
        }
        
        handler = handlers.get(intent, self.handle_general)
        return handler(query)

# Initialize chatbot
chatbot = JewelryMLChatbot()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'jewelry_items': chatbot.knowledge_base.get('total_jewelry', 0),
        'diamonds': chatbot.knowledge_base.get('total_diamonds', 0)
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        response = chatbot.generate_response(message)
        
        return jsonify({
            'response': response,
            'intent': chatbot.classify_intent(message)
        })
    
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("ML JEWELRY CHATBOT SERVER")
    print("="*60)
    print(f"Knowledge Base: {chatbot.knowledge_base.get('total_jewelry', 0):,} jewelry, {chatbot.knowledge_base.get('total_diamonds', 0):,} diamonds")
    print("Server: http://localhost:5000")
    print("Health: http://localhost:5000/health")
    print("Chat: POST http://localhost:5000/chat")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
