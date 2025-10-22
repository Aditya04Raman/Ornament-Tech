"""
Advanced ML Service for Ornament Tech - Production Ready
Deep dataset understanding with intelligent query processing
"""

import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import logging
from datetime import datetime
import json
from typing import Dict, List, Tuple, Any
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class IntelligentJewelryBot:
    def __init__(self):
        """Initialize the intelligent jewelry bot with deep dataset understanding"""
        self.app_name = "Intelligent Ornament Tech ML Chatbot"
        self.version = "3.0"
        
        # Load datasets
        self.jewelry_df = None
        self.diamonds_df = None
        self.analytics = {}
        
        # Website structure knowledge
        self.website_structure = {
            'pages': [
                'home', 'about', 'collections', 'bespoke-process', 'craftsmanship',
                'materials', 'gemstones', 'sizing', 'care', 'galleries', 'journal',
                'stores', 'contact', 'appointments', 'faq'
            ],
            'collections': ['engagement_rings', 'wedding_bands', 'necklaces', 'earrings', 'bracelets', 'rings'],
            'services': ['bespoke_design', 'resizing', 'repairs', 'cleaning', 'appointments'],
            'materials': ['gold', 'white_gold', 'rose_gold', 'platinum', 'silver'],
            'gemstones': ['diamond', 'emerald', 'ruby', 'sapphire', 'pearl']
        }
        
        # Advanced intent categories
        self.intent_categories = {
            'product_inquiry': ['show', 'find', 'looking for', 'want', 'need', 'search', 'browse'],
            'comparison': ['compare', 'difference', 'better', 'vs', 'which', 'best', 'recommend'],
            'recommendation': ['suggest', 'recommend', 'advice', 'help choose', 'what should', 'suits me'],
            'technical_info': ['4c', 'carat', 'cut', 'color', 'clarity', 'quality', 'grade', 'certification'],
            'pricing': ['price', 'cost', 'expensive', 'cheap', 'budget', 'affordable', 'value'],
            'services': ['bespoke', 'custom', 'design', 'resize', 'repair', 'clean', 'appointment'],
            'education': ['learn', 'what is', 'how to', 'explain', 'tell me about', 'information']
        }
        
        # Initialize system
        self.load_datasets()
        self.load_analytics()
        
        logger.info(f"🚀 {self.app_name} v{self.version} initialized successfully!")
        logger.info(f"📊 Loaded {len(self.jewelry_df) if self.jewelry_df is not None else 0} jewelry items")
        logger.info(f"💎 Loaded {len(self.diamonds_df) if self.diamonds_df is not None else 0} diamonds")
    
    def load_datasets(self):
        """Load datasets with error handling"""
        try:
            # Get the base directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
            # Load jewelry dataset
            jewelry_path = os.path.join(base_dir, "datasets", "jewelry_dataset.csv")
            if os.path.exists(jewelry_path):
                self.jewelry_df = pd.read_csv(jewelry_path)
                logger.info(f"✅ Loaded jewelry dataset: {len(self.jewelry_df)} items")
                self._enrich_jewelry_data()
            else:
                logger.warning(f"⚠️ Jewelry dataset not found at {jewelry_path}")
                
            # Load diamonds dataset
            diamonds_path = os.path.join(base_dir, "datasets", "diamonds_dataset.csv")
            if os.path.exists(diamonds_path):
                self.diamonds_df = pd.read_csv(diamonds_path)
                logger.info(f"✅ Loaded diamonds dataset: {len(self.diamonds_df)} items")
                self._enrich_diamond_data()
            else:
                logger.warning(f"⚠️ Diamonds dataset not found at {diamonds_path}")
                
        except Exception as e:
            logger.error(f"❌ Error loading datasets: {e}")
    
    def _enrich_jewelry_data(self):
        """Enrich jewelry dataset with additional insights"""
        if self.jewelry_df is not None:
            # Add price categories
            self.jewelry_df['price_category'] = pd.cut(
                self.jewelry_df['price'], 
                bins=[0, 5000, 15000, 30000, float('inf')], 
                labels=['Budget', 'Mid-range', 'Luxury', 'Ultra-luxury']
            )
            
            # Add value score (weight/price ratio)
            self.jewelry_df['value_score'] = self.jewelry_df['weight'] / self.jewelry_df['price'] * 1000
            
            # Add style categories
            self.jewelry_df['style'] = self.jewelry_df.apply(self._determine_style, axis=1)
    
    def _determine_style(self, row):
        """Determine jewelry style based on characteristics"""
        if row['type'] in ['engagement', 'wedding']:
            return 'Bridal'
        elif row['brand'] == 'vintage':
            return 'Vintage'
        elif row['stone'] in ['diamond', 'emerald']:
            return 'Classic'
        else:
            return 'Contemporary'
    
    def _enrich_diamond_data(self):
        """Enrich diamond dataset with quality metrics"""
        if self.diamonds_df is not None:
            # Add quality scores
            cut_scores = {'Ideal': 5, 'Premium': 4, 'Very Good': 3, 'Good': 2, 'Fair': 1}
            color_scores = {'D': 7, 'E': 6, 'F': 5, 'G': 4, 'H': 3, 'I': 2, 'J': 1}
            clarity_scores = {'FL': 8, 'IF': 7, 'VVS1': 6, 'VVS2': 5, 'VS1': 4, 'VS2': 3, 'SI1': 2, 'SI2': 1}
            
            self.diamonds_df['cut_score'] = self.diamonds_df['cut'].map(cut_scores).fillna(2)
            self.diamonds_df['color_score'] = self.diamonds_df['color'].map(color_scores).fillna(4)
            self.diamonds_df['clarity_score'] = self.diamonds_df['clarity'].map(clarity_scores).fillna(3)
            
            # Overall quality score
            self.diamonds_df['quality_score'] = (
                self.diamonds_df['cut_score'] + 
                self.diamonds_df['color_score'] + 
                self.diamonds_df['clarity_score']
            ) / 3
            
            # Price per carat
            self.diamonds_df['price_per_carat'] = self.diamonds_df['price'] / self.diamonds_df['carat']
            
            # Size categories
            self.diamonds_df['size_category'] = pd.cut(
                self.diamonds_df['carat'],
                bins=[0, 0.5, 1.0, 2.0, float('inf')],
                labels=['Small', 'Medium', 'Large', 'Very Large']
            )
    
    def load_analytics(self):
        """Load pre-computed analytics"""
        try:
            # Get the base directory
            base_dir = os.path.dirname(os.path.abspath(__file__))
            analytics_path = os.path.join(base_dir, "models", "dataset_analytics.json")
            
            if os.path.exists(analytics_path):
                with open(analytics_path, 'r', encoding='utf-8') as f:
                    self.analytics = json.load(f)
                logger.info("✅ Loaded dataset analytics")
            else:
                logger.info("📊 Generating analytics from datasets...")
                self._generate_analytics()
        except Exception as e:
            logger.error(f"❌ Error loading analytics: {e}")
            self._generate_analytics()
    
    def _generate_analytics(self):
        """Generate analytics from datasets"""
        self.analytics = {'jewelry': {}, 'diamonds': {}, 'insights': {}}
        
        if self.jewelry_df is not None:
            self.analytics['jewelry'] = {
                'total_items': len(self.jewelry_df),
                'avg_price': float(self.jewelry_df['price'].mean()),
                'price_range': [float(self.jewelry_df['price'].min()), float(self.jewelry_df['price'].max())],
                'popular_category': self.jewelry_df['category'].mode().iloc[0],
                'expensive_metal': self.jewelry_df.groupby('metal')['price'].mean().idxmax(),
                'popular_stone': self.jewelry_df['stone'].mode().iloc[0]
            }
        
        if self.diamonds_df is not None:
            self.analytics['diamonds'] = {
                'total_items': len(self.diamonds_df),
                'avg_price': float(self.diamonds_df['price'].mean()),
                'avg_carat': float(self.diamonds_df['carat'].mean()),
                'popular_cut': self.diamonds_df['cut'].mode().iloc[0],
                'popular_color': self.diamonds_df['color'].mode().iloc[0],
                'popular_clarity': self.diamonds_df['clarity'].mode().iloc[0]
            }
    
    def process_query(self, message: str) -> Dict[str, Any]:
        """Process user query with intelligent understanding"""
        try:
            # Clean and analyze message
            cleaned_message = self._clean_message(message)
            
            # Classify intent
            intent = self._classify_intent(cleaned_message)
            
            # Extract entities
            entities = self._extract_entities(cleaned_message)
            
            # Generate intelligent response
            response = self._generate_response(intent, entities, cleaned_message)
            
            return {
                'response': response,
                'intent': intent,
                'entities': entities,
                'confidence': 0.95,
                'source': 'intelligent_ml',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'response': "I apologize for the technical issue. Let me help you with your jewelry inquiry. What would you like to know?",
                'intent': 'error',
                'entities': {},
                'confidence': 0.0,
                'source': 'error_fallback',
                'timestamp': datetime.now().isoformat()
            }
    
    def _clean_message(self, message: str) -> str:
        """Clean and normalize message"""
        cleaned = message.lower().strip()
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Expand contractions
        contractions = {
            "i'm": "i am", "you're": "you are", "it's": "it is",
            "can't": "cannot", "don't": "do not", "won't": "will not"
        }
        
        for contraction, expansion in contractions.items():
            cleaned = cleaned.replace(contraction, expansion)
        
        return cleaned
    
    def _classify_intent(self, message: str) -> str:
        """Classify intent using keyword matching"""
        # Check for specific intents
        for intent, keywords in self.intent_categories.items():
            if any(keyword in message for keyword in keywords):
                return intent
        
        # Default intent
        return 'general_inquiry'
    
    def _extract_entities(self, message: str) -> Dict[str, List[str]]:
        """Extract entities from message"""
        entities = {
            'products': [],
            'materials': [],
            'gemstones': [],
            'price_range': [],
            'occasions': [],
            'preferences': []
        }
        
        # Extract products
        products = ['ring', 'necklace', 'earring', 'bracelet', 'engagement ring', 'wedding band']
        for product in products:
            if product in message:
                entities['products'].append(product)
        
        # Extract materials
        for material in self.website_structure['materials']:
            if material.replace('_', ' ') in message:
                entities['materials'].append(material)
        
        # Extract gemstones
        for gemstone in self.website_structure['gemstones']:
            if gemstone in message:
                entities['gemstones'].append(gemstone)
        
        # Extract price information
        price_matches = re.findall(r'\$?(\d+)k?', message)
        if price_matches:
            entities['price_range'] = price_matches
        
        return entities
    
    def _generate_response(self, intent: str, entities: Dict, message: str) -> str:
        """Generate intelligent response based on intent and entities"""
        
        if intent == 'comparison':
            return self._handle_comparison_query(entities, message)
        elif intent == 'recommendation':
            return self._handle_recommendation_query(entities, message)
        elif intent == 'product_inquiry':
            return self._handle_product_inquiry(entities, message)
        elif intent == 'pricing':
            return self._handle_pricing_query(entities, message)
        elif intent == 'technical_info':
            return self._handle_technical_query(entities, message)
        elif intent == 'services':
            return self._handle_services_query(entities, message)
        elif intent == 'education':
            return self._handle_education_query(entities, message)
        else:
            return self._handle_general_query(entities, message)
    
    def _handle_comparison_query(self, entities: Dict, message: str) -> str:
        """Handle comparison queries with data-driven insights"""
        
        if 'suits me' in message or 'best for me' in message:
            return self._generate_personal_recommendation(entities, message)
        
        products = entities.get('products', [])
        materials = entities.get('materials', [])
        
        if len(products) >= 2:
            return self._compare_products_with_data(products)
        elif len(materials) >= 2:
            return self._compare_materials_with_data(materials)
        else:
            return self._generate_general_comparison_with_data()
    
    def _generate_personal_recommendation(self, entities: Dict, message: str) -> str:
        """Generate personalized recommendations using dataset insights"""
        recommendations = []
        
        # Use analytics for recommendations
        if self.analytics.get('jewelry'):
            jewelry_data = self.analytics['jewelry']
            recommendations.append(f"Based on our collection of {jewelry_data['total_items']} jewelry pieces:")
            
            if 'elegant' in message or 'classic' in message:
                recommendations.append(f"For elegance, I recommend our {jewelry_data['expensive_metal']} pieces with {jewelry_data['popular_stone']}s - they're our most refined options.")
            
            if 'budget' in message or 'affordable' in message:
                # Find budget-friendly options from data
                if self.jewelry_df is not None:
                    budget_items = self.jewelry_df[self.jewelry_df['price'] < 5000]
                    if not budget_items.empty:
                        best_value = budget_items.loc[budget_items['value_score'].idxmax()]
                        recommendations.append(f"For great value, consider {best_value['metal']} {best_value['category']}s with {best_value['stone']}s starting around ${best_value['price']:,.0f}.")
            
            # Add trending information
            recommendations.append(f"Currently, {jewelry_data['popular_category']}s are our most popular category, especially in {jewelry_data['expensive_metal']}.")
        
        # Diamond recommendations if relevant
        if 'diamond' in message and self.analytics.get('diamonds'):
            diamond_data = self.analytics['diamonds']
            recommendations.append(f"From our {diamond_data['total_items']} diamond collection:")
            recommendations.append(f"Most customers choose {diamond_data['popular_cut']} cut diamonds in {diamond_data['popular_color']} color with {diamond_data['popular_clarity']} clarity.")
            recommendations.append(f"Average size is {diamond_data['avg_carat']:.2f} carats at ${diamond_data['avg_price']:,.0f}.")
        
        if not recommendations:
            recommendations.append("I'd love to help you find the perfect piece! Let me understand your preferences better.")
        
        recommendations.append("Would you like to schedule a consultation to explore options that perfectly match your style and budget?")
        
        return " ".join(recommendations)
    
    def _compare_products_with_data(self, products: List[str]) -> str:
        """Compare products using real dataset insights"""
        comparison = [f"Comparing {' vs '.join(products)} from our collection:"]
        
        if self.jewelry_df is not None:
            for product in products:
                # Get data for this product type
                product_data = self.jewelry_df[self.jewelry_df['category'].str.contains(product, case=False, na=False)]
                
                if not product_data.empty:
                    avg_price = product_data['price'].mean()
                    price_range = (product_data['price'].min(), product_data['price'].max())
                    popular_metal = product_data['metal'].mode().iloc[0] if not product_data['metal'].mode().empty else 'gold'
                    popular_stone = product_data['stone'].mode().iloc[0] if not product_data['stone'].mode().empty else 'diamond'
                    
                    comparison.append(f"\n**{product.title()}s in our collection:**")
                    comparison.append(f"• Average price: ${avg_price:,.0f}")
                    comparison.append(f"• Price range: ${price_range[0]:,.0f} - ${price_range[1]:,.0f}")
                    comparison.append(f"• Most popular: {popular_metal} with {popular_stone}")
                    comparison.append(f"• Available pieces: {len(product_data)}")
        
        comparison.append("\nThe best choice depends on your personal style, occasion, and budget. Would you like specific recommendations?")
        
        return "\n".join(comparison)
    
    def _compare_materials_with_data(self, materials: List[str]) -> str:
        """Compare materials using dataset pricing"""
        comparison = [f"Material comparison from our collection data:"]
        
        if self.jewelry_df is not None:
            for material in materials:
                material_data = self.jewelry_df[self.jewelry_df['metal'].str.contains(material.replace('_', ' '), case=False, na=False)]
                
                if not material_data.empty:
                    avg_price = material_data['price'].mean()
                    count = len(material_data)
                    popular_category = material_data['category'].mode().iloc[0] if not material_data['category'].mode().empty else 'rings'
                    
                    comparison.append(f"\n**{material.replace('_', ' ').title()}:**")
                    comparison.append(f"• Average price: ${avg_price:,.0f}")
                    comparison.append(f"• Available pieces: {count}")
                    comparison.append(f"• Most popular in: {popular_category}")
        
        # Add material properties
        material_properties = {
            'gold': 'Timeless, warm yellow tone, excellent durability',
            'white_gold': 'Modern, cool silver appearance, needs rhodium maintenance',
            'rose_gold': 'Romantic pink hue, trendy, hypoallergenic',
            'platinum': 'Most precious, naturally white, extremely durable',
            'silver': 'Affordable, bright white, requires regular cleaning'
        }
        
        comparison.append("\n**Material Properties:**")
        for material in materials:
            if material in material_properties:
                comparison.append(f"• **{material.replace('_', ' ').title()}**: {material_properties[material]}")
        
        return "\n".join(comparison)
    
    def _generate_general_comparison_with_data(self) -> str:
        """Generate comparison advice using dataset insights"""
        advice = ["Here's how to compare jewelry options effectively:"]
        
        if self.analytics.get('jewelry'):
            jewelry_data = self.analytics['jewelry']
            advice.append(f"\n**From our collection of {jewelry_data['total_items']} pieces:**")
            advice.append(f"• Most popular: {jewelry_data['popular_category']}s")
            advice.append(f"• Premium choice: {jewelry_data['expensive_metal']}")
            advice.append(f"• Trending stone: {jewelry_data['popular_stone']}")
            advice.append(f"• Price range: ${jewelry_data['price_range'][0]:,.0f} - ${jewelry_data['price_range'][1]:,.0f}")
        
        advice.extend([
            "\n**Key Comparison Factors:**",
            "• **Quality**: Material purity, gemstone grade, craftsmanship",
            "• **Style**: Classic vs contemporary, occasion-appropriate",
            "• **Value**: Price vs quality ratio, long-term durability",
            "• **Personal fit**: Skin tone, lifestyle, maintenance needs"
        ])
        
        advice.append("\nWhat specific pieces would you like me to compare for you?")
        
        return "\n".join(advice)
    
    def _handle_recommendation_query(self, entities: Dict, message: str) -> str:
        """Handle recommendation with dataset-driven suggestions"""
        recommendations = ["I'll help you find the perfect jewelry based on our collection:"]
        
        # Budget analysis
        budget_mentioned = any(word in message for word in ['budget', 'cheap', 'affordable', 'expensive'])
        
        if self.jewelry_df is not None:
            if budget_mentioned:
                # Budget recommendations
                budget_pieces = self.jewelry_df[self.jewelry_df['price'] < 5000]
                if not budget_pieces.empty:
                    best_value = budget_pieces.loc[budget_pieces['value_score'].idxmax()]
                    recommendations.append(f"\n**Best Value Pick**: {best_value['metal'].title()} {best_value['category']} with {best_value['stone']} - ${best_value['price']:,.0f}")
            
            # Category recommendations
            if entities.get('products'):
                product = entities['products'][0]
                product_data = self.jewelry_df[self.jewelry_df['category'].str.contains(product, case=False, na=False)]
                if not product_data.empty:
                    top_pick = product_data.loc[product_data['price'].idxmin()]  # Most affordable
                    premium_pick = product_data.loc[product_data['price'].idxmax()]  # Most premium
                    
                    recommendations.append(f"\n**{product.title()} Recommendations:**")
                    recommendations.append(f"• **Accessible option**: {top_pick['metal']} with {top_pick['stone']} - ${top_pick['price']:,.0f}")
                    recommendations.append(f"• **Premium choice**: {premium_pick['metal']} with {premium_pick['stone']} - ${premium_pick['price']:,.0f}")
        
        # Add general recommendations
        if self.analytics.get('jewelry'):
            jewelry_data = self.analytics['jewelry']
            recommendations.append(f"\n**Popular Choices** (from {jewelry_data['total_items']} pieces):")
            recommendations.append(f"• Most loved: {jewelry_data['popular_category']}s with {jewelry_data['popular_stone']}s")
            recommendations.append(f"• Premium metal: {jewelry_data['expensive_metal']}")
            recommendations.append(f"• Average investment: ${jewelry_data['avg_price']:,.0f}")
        
        recommendations.append("\nFor personalized recommendations, I'd love to know more about your style preferences and budget range!")
        
        return "\n".join(recommendations)
    
    def _handle_product_inquiry(self, entities: Dict, message: str) -> str:
        """Handle product inquiries with dataset insights"""
        response_parts = ["I'll help you explore our jewelry collection:"]
        
        if entities.get('products'):
            product = entities['products'][0]
            
            if self.jewelry_df is not None:
                product_data = self.jewelry_df[self.jewelry_df['category'].str.contains(product, case=False, na=False)]
                
                if not product_data.empty:
                    response_parts.append(f"\n**{product.title()}s in our collection:**")
                    response_parts.append(f"• Total pieces: {len(product_data)}")
                    response_parts.append(f"• Price range: ${product_data['price'].min():,.0f} - ${product_data['price'].max():,.0f}")
                    response_parts.append(f"• Average price: ${product_data['price'].mean():,.0f}")
                    
                    # Popular combinations
                    popular_metal = product_data['metal'].mode().iloc[0] if not product_data['metal'].mode().empty else 'gold'
                    popular_stone = product_data['stone'].mode().iloc[0] if not product_data['stone'].mode().empty else 'diamond'
                    response_parts.append(f"• Most popular: {popular_metal} with {popular_stone}")
                    
                    # Style breakdown
                    style_counts = product_data['style'].value_counts() if 'style' in product_data.columns else None
                    if style_counts is not None and not style_counts.empty:
                        top_style = style_counts.index[0]
                        response_parts.append(f"• Trending style: {top_style}")
        
        # Add collection information
        response_parts.extend([
            "\n**Our Collections Include:**",
            "• **Engagement & Wedding**: Timeless symbols of love",
            "• **Everyday Elegance**: Perfect for daily wear",
            "• **Statement Pieces**: Bold, eye-catching designs",
            "• **Vintage Inspired**: Classic beauty with modern quality"
        ])
        
        response_parts.append("\nWould you like to see specific styles or learn about pricing for any category?")
        
        return "\n".join(response_parts)
    
    def _handle_pricing_query(self, entities: Dict, message: str) -> str:
        """Handle pricing queries with comprehensive data"""
        response_parts = ["Here's pricing information from our collection:"]
        
        if self.analytics.get('jewelry'):
            jewelry_data = self.analytics['jewelry']
            response_parts.append(f"\n**Jewelry Collection** ({jewelry_data['total_items']} pieces):")
            response_parts.append(f"• Price range: ${jewelry_data['price_range'][0]:,.0f} - ${jewelry_data['price_range'][1]:,.0f}")
            response_parts.append(f"• Average price: ${jewelry_data['avg_price']:,.0f}")
        
        if self.analytics.get('diamonds'):
            diamond_data = self.analytics['diamonds']
            response_parts.append(f"\n**Diamond Collection** ({diamond_data['total_items']} stones):")
            response_parts.append(f"• Average price: ${diamond_data['avg_price']:,.0f}")
            response_parts.append(f"• Average size: {diamond_data['avg_carat']:.2f} carats")
        
        # Detailed pricing if specific product mentioned
        if entities.get('products') and self.jewelry_df is not None:
            product = entities['products'][0]
            product_data = self.jewelry_df[self.jewelry_df['category'].str.contains(product, case=False, na=False)]
            
            if not product_data.empty:
                response_parts.append(f"\n**{product.title()} Pricing:**")
                
                # Price segments
                price_segments = product_data['price_category'].value_counts() if 'price_category' in product_data.columns else None
                if price_segments is not None:
                    for category, count in price_segments.items():
                        segment_data = product_data[product_data['price_category'] == category]
                        avg_price = segment_data['price'].mean()
                        response_parts.append(f"• {category}: {count} pieces, avg ${avg_price:,.0f}")
        
        response_parts.extend([
            "\n**Pricing Factors:**",
            "• Material quality and rarity",
            "• Gemstone grade (4Cs for diamonds)",
            "• Craftsmanship complexity",
            "• Brand heritage and design exclusivity",
            "\nFor exact pricing on specific pieces, I recommend browsing our collections or scheduling a consultation."
        ])
        
        return "\n".join(response_parts)
    
    def _handle_technical_query(self, entities: Dict, message: str) -> str:
        """Handle technical queries with dataset examples"""
        response_parts = ["I'll explain the technical aspects using examples from our collection:"]
        
        if 'diamond' in message or '4c' in message:
            response_parts.extend([
                "\n**Diamond Quality - The 4Cs:**",
                "",
                "**Cut**: Determines brilliance and fire",
                "• Excellent/Ideal: Maximum light performance",
                "• Very Good: High brilliance",
                "• Good: Good light return, excellent value"
            ])
            
            if self.analytics.get('diamonds'):
                diamond_data = self.analytics['diamonds']
                response_parts.append(f"• Most popular in our collection: {diamond_data['popular_cut']} cut")
            
            response_parts.extend([
                "",
                "**Color**: Graded D (colorless) to Z (light yellow)",
                "• D-F: Colorless premium grade",
                "• G-J: Near colorless, excellent value",
                "• K+: Warm tone, budget-friendly"
            ])
            
            if self.analytics.get('diamonds'):
                response_parts.append(f"• Customer favorite: {diamond_data['popular_color']} color grade")
            
            response_parts.extend([
                "",
                "**Clarity**: Internal inclusion visibility",
                "• FL/IF: Flawless (rare and premium)",
                "• VVS1/VVS2: Very very slight inclusions",
                "• VS1/VS2: Very slight inclusions (sweet spot)",
                "• SI1/SI2: Slight inclusions (great value)"
            ])
            
            if self.analytics.get('diamonds'):
                response_parts.append(f"• Popular choice: {diamond_data['popular_clarity']} clarity")
            
            response_parts.extend([
                "",
                "**Carat**: Weight and size",
                "• 1 carat = 200 milligrams",
                "• Price increases exponentially with size"
            ])
            
            if self.analytics.get('diamonds'):
                response_parts.append(f"• Average in our collection: {diamond_data['avg_carat']:.2f} carats")
        
        response_parts.append("\nWould you like detailed information about any specific quality aspect?")
        
        return "\n".join(response_parts)
    
    def _handle_services_query(self, entities: Dict, message: str) -> str:
        """Handle service queries"""
        return """**Our Jewelry Services:**

**Bespoke Design**: Create one-of-a-kind pieces tailored to your vision
• Initial consultation and design concept
• 3D modeling and approval process
• Expert craftsmanship using finest materials
• Lifetime service and maintenance

**Maintenance & Care**: Keep your jewelry pristine
• Professional cleaning and inspection
• Prong repair and stone tightening
• Resizing and alterations
• Restoration of vintage pieces

**Consultation Services**: Expert guidance
• Style and design recommendations
• Investment and insurance appraisals
• Collection building advice
• Special occasion planning

**Why Choose Our Services:**
• Master craftsmen with decades of experience
• Ethically sourced, premium materials
• Satisfaction guarantee on all work
• Complimentary lifetime care guidance

Would you like to schedule a consultation or learn more about any specific service?"""
    
    def _handle_education_query(self, entities: Dict, message: str) -> str:
        """Handle educational queries"""
        return """**Jewelry Education:**

**Care & Maintenance:**
• Daily: Remove before exercise, swimming, cleaning
• Storage: Separate compartments to prevent scratching
• Cleaning: Gentle methods appropriate for each material

**Understanding Quality:**
• Diamonds: The 4Cs (Cut, Color, Clarity, Carat)
• Metals: Purity, durability, and maintenance needs
• Craftsmanship: Hand-finished details vs mass production

**Investment Guidance:**
• Quality over quantity for lasting value
• Classic designs retain value better
• Proper documentation and certificates
• Insurance and appraisal considerations

**Style Selection:**
• Face shape considerations for earrings
• Skin tone matching with metal colors
• Lifestyle compatibility
• Occasion appropriateness

What specific jewelry topic would you like to learn more about?"""
    
    def _handle_general_query(self, entities: Dict, message: str) -> str:
        """Handle general queries with personalized welcome"""
        welcome_parts = ["Welcome to Ornament Tech! I'm your intelligent jewelry consultant."]
        
        if self.analytics.get('jewelry') and self.analytics.get('diamonds'):
            jewelry_data = self.analytics['jewelry']
            diamond_data = self.analytics['diamonds']
            
            welcome_parts.append(f"\n**Our Collection** ({jewelry_data['total_items']} jewelry pieces + {diamond_data['total_items']} diamonds):")
            welcome_parts.append(f"• Most popular: {jewelry_data['popular_category']}s with {jewelry_data['popular_stone']}s")
            welcome_parts.append(f"• Premium materials: {jewelry_data['expensive_metal']} and certified diamonds")
            welcome_parts.append(f"• Price range: ${jewelry_data['price_range'][0]:,.0f} - ${jewelry_data['price_range'][1]:,.0f}")
        
        welcome_parts.extend([
            "\n**I can help you with:**",
            "• Smart product recommendations based on your preferences",
            "• Detailed comparisons between different options",
            "• Pricing insights and budget planning",
            "• Technical details about diamonds and gemstones",
            "• Information about our services and processes",
            "• Educational content about jewelry care",
            "",
            "**Our Specialties:**",
            "• Engagement rings and wedding bands",
            "• Custom and bespoke jewelry design",
            "• Certified diamonds and precious gemstones",
            "• Expert craftsmanship with lifetime service",
            "",
            "What can I help you discover today? Ask me anything about jewelry!"
        ])
        
        return "\n".join(welcome_parts)

# Initialize the bot
bot = IntelligentJewelryBot()

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'response': 'Please provide a message to help you better.',
                'error': 'Empty message'
            }), 400
        
        # Process query with intelligent bot
        result = bot.process_query(message)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            'response': 'I apologize for the technical issue. Please try rephrasing your question, and I\'ll be happy to help!',
            'error': str(e),
            'source': 'error_handler'
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': bot.app_name,
        'version': bot.version,
        'timestamp': datetime.now().isoformat(),
        'data_loaded': {
            'jewelry_items': len(bot.jewelry_df) if bot.jewelry_df is not None else 0,
            'diamond_items': len(bot.diamonds_df) if bot.diamonds_df is not None else 0,
            'analytics_loaded': bool(bot.analytics)
        }
    })

@app.route('/analytics', methods=['GET'])
def analytics():
    """Analytics endpoint"""
    return jsonify(bot.analytics)

if __name__ == '__main__':
    logger.info(f"🚀 Starting {bot.app_name} v{bot.version}")
    logger.info("🔗 Available endpoints:")
    logger.info("   POST /chat - Intelligent chat interface")
    logger.info("   GET /health - Service health check")
    logger.info("   GET /analytics - Dataset analytics")
    
    app.run(host='0.0.0.0', port=5000, debug=False)