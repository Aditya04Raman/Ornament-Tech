"""
Advanced ML Service for Ornament Tech
Deep dataset and website structure understanding with intelligent query processing
"""

import os
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
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

class AdvancedJewelryBot:
    def __init__(self):
        """Initialize the advanced jewelry bot with deep dataset understanding"""
        self.app_name = "Advanced Ornament Tech ML Chatbot"
        self.version = "2.0"
        
        # Load and process datasets
        self.jewelry_df = None
        self.diamonds_df = None
        self.combined_knowledge = {}
        
        # ML models and components
        self.tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english', ngram_range=(1, 3))
        self.intent_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.diamond_recommender = None
        self.jewelry_recommender = None
        
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
        
        # Advanced intent categories with sub-intents
        self.intent_categories = {
            'product_inquiry': {
                'keywords': ['show', 'find', 'looking for', 'want', 'need', 'search', 'browse'],
                'sub_intents': ['specific_product', 'category_browse', 'price_range', 'material_preference']
            },
            'comparison': {
                'keywords': ['compare', 'difference', 'better', 'vs', 'which', 'best', 'recommend'],
                'sub_intents': ['product_comparison', 'material_comparison', 'price_comparison', 'quality_comparison']
            },
            'recommendation': {
                'keywords': ['suggest', 'recommend', 'advice', 'help choose', 'what should', 'suits me'],
                'sub_intents': ['personal_recommendation', 'occasion_based', 'budget_based', 'style_based']
            },
            'technical_info': {
                'keywords': ['4c', 'carat', 'cut', 'color', 'clarity', 'quality', 'grade', 'certification'],
                'sub_intents': ['diamond_specs', 'quality_info', 'certification', 'grading']
            },
            'pricing': {
                'keywords': ['price', 'cost', 'expensive', 'cheap', 'budget', 'affordable', 'value'],
                'sub_intents': ['price_inquiry', 'budget_options', 'value_comparison', 'payment_options']
            },
            'services': {
                'keywords': ['bespoke', 'custom', 'design', 'resize', 'repair', 'clean', 'appointment'],
                'sub_intents': ['bespoke_design', 'maintenance', 'appointments', 'consultations']
            },
            'education': {
                'keywords': ['learn', 'what is', 'how to', 'explain', 'tell me about', 'information'],
                'sub_intents': ['jewelry_education', 'gemstone_education', 'care_instructions', 'sizing_guide']
            }
        }
        
        # Initialize the system
        self.load_datasets()
        self.process_datasets()
        self.train_models()
        
        logger.info(f"🚀 {self.app_name} v{self.version} initialized successfully!")
        logger.info(f"📊 Loaded {len(self.jewelry_df)} jewelry items and {len(self.diamonds_df)} diamonds")
    
    def load_datasets(self):
        """Load both jewelry and diamond datasets"""
        try:
            # Load jewelry dataset
            jewelry_path = "../datasets/jewelry_dataset.csv"
            if os.path.exists(jewelry_path):
                self.jewelry_df = pd.read_csv(jewelry_path)
                logger.info(f"✅ Loaded jewelry dataset: {len(self.jewelry_df)} items")
            else:
                logger.warning("⚠️ Jewelry dataset not found")
                
            # Load diamonds dataset
            diamonds_path = "../datasets/diamonds_dataset.csv"
            if os.path.exists(diamonds_path):
                self.diamonds_df = pd.read_csv(diamonds_path)
                logger.info(f"✅ Loaded diamonds dataset: {len(self.diamonds_df)} items")
            else:
                logger.warning("⚠️ Diamonds dataset not found")
                
        except Exception as e:
            logger.error(f"❌ Error loading datasets: {e}")
            # Create dummy datasets if files not found
            self.create_dummy_datasets()
    
    def create_dummy_datasets(self):
        """Create dummy datasets for testing"""
        logger.info("Creating dummy datasets...")
        
        # Dummy jewelry data
        self.jewelry_df = pd.DataFrame({
            'category': ['ring', 'necklace', 'earring', 'bracelet'] * 100,
            'type': ['engagement', 'statement', 'stud', 'tennis'] * 100,
            'metal': ['gold', 'platinum', 'silver', 'white_gold'] * 100,
            'stone': ['diamond', 'emerald', 'ruby', 'sapphire'] * 100,
            'weight': np.random.uniform(5, 50, 400),
            'size': np.random.uniform(5, 12, 400),
            'brand': ['designer', 'vintage', 'modern', 'classic'] * 100,
            'price': np.random.uniform(1000, 50000, 400)
        })
        
        # Dummy diamond data
        self.diamonds_df = pd.DataFrame({
            'carat': np.random.uniform(0.2, 3.0, 1000),
            'cut': np.random.choice(['Ideal', 'Premium', 'Very Good', 'Good', 'Fair'], 1000),
            'color': np.random.choice(['D', 'E', 'F', 'G', 'H', 'I', 'J'], 1000),
            'clarity': np.random.choice(['FL', 'IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2'], 1000),
            'depth': np.random.uniform(55, 70, 1000),
            'table': np.random.uniform(50, 70, 1000),
            'price': np.random.uniform(300, 20000, 1000),
            'x': np.random.uniform(3, 8, 1000),
            'y': np.random.uniform(3, 8, 1000),
            'z': np.random.uniform(2, 5, 1000)
        })
    
    def process_datasets(self):
        """Process and enrich datasets with additional insights"""
        if self.jewelry_df is not None:
            # Add price categories
            self.jewelry_df['price_category'] = pd.cut(
                self.jewelry_df['price'], 
                bins=[0, 5000, 15000, 30000, float('inf')], 
                labels=['Budget', 'Mid-range', 'Luxury', 'Ultra-luxury']
            )
            
            # Add style categories
            self.jewelry_df['style'] = self.jewelry_df.apply(self._determine_style, axis=1)
            
        if self.diamonds_df is not None:
            # Add quality score
            self.diamonds_df['quality_score'] = self._calculate_diamond_quality()
            
            # Add price per carat
            self.diamonds_df['price_per_carat'] = self.diamonds_df['price'] / self.diamonds_df['carat']
            
            # Add size category
            self.diamonds_df['size_category'] = pd.cut(
                self.diamonds_df['carat'],
                bins=[0, 0.5, 1.0, 2.0, float('inf')],
                labels=['Small', 'Medium', 'Large', 'Very Large']
            )
    
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
    
    def _calculate_diamond_quality(self):
        """Calculate diamond quality score based on 4Cs"""
        if self.diamonds_df is None:
            return []
            
        # Scoring system for each factor
        cut_scores = {'Ideal': 5, 'Premium': 4, 'Very Good': 3, 'Good': 2, 'Fair': 1}
        color_scores = {'D': 7, 'E': 6, 'F': 5, 'G': 4, 'H': 3, 'I': 2, 'J': 1}
        clarity_scores = {'FL': 8, 'IF': 7, 'VVS1': 6, 'VVS2': 5, 'VS1': 4, 'VS2': 3, 'SI1': 2, 'SI2': 1}
        
        scores = []
        for _, row in self.diamonds_df.iterrows():
            cut_score = cut_scores.get(row['cut'], 1)
            color_score = color_scores.get(row['color'], 1)
            clarity_score = clarity_scores.get(row['clarity'], 1)
            carat_score = min(row['carat'] * 2, 5)  # Cap at 5
            
            total_score = (cut_score + color_score + clarity_score + carat_score) / 4
            scores.append(round(total_score, 2))
        
        return scores
    
    def train_models(self):
        """Train ML models for intelligent responses"""
        try:
            # Create training data for intent classification
            training_texts = []
            training_labels = []
            
            # Generate training examples for each intent
            for intent, data in self.intent_categories.items():
                for keyword in data['keywords']:
                    for product in ['ring', 'necklace', 'earring', 'bracelet', 'diamond']:
                        training_texts.append(f"{keyword} {product}")
                        training_labels.append(intent)
                        
                        # Add variations
                        training_texts.append(f"I want to {keyword} a {product}")
                        training_labels.append(intent)
                        
                        training_texts.append(f"Can you {keyword} {product}s?")
                        training_labels.append(intent)
            
            # Train TF-IDF vectorizer
            X = self.tfidf_vectorizer.fit_transform(training_texts)
            
            # Train intent classifier
            self.intent_classifier.fit(X, training_labels)
            
            # Train product recommenders if data is available
            if self.jewelry_df is not None and len(self.jewelry_df) > 0:
                self._train_jewelry_recommender()
            
            if self.diamonds_df is not None and len(self.diamonds_df) > 0:
                self._train_diamond_recommender()
                
            logger.info("✅ ML models trained successfully")
            
        except Exception as e:
            logger.error(f"❌ Error training models: {e}")
    
    def _train_jewelry_recommender(self):
        """Train jewelry recommendation model"""
        try:
            # Prepare features for jewelry recommendation
            features = []
            for _, row in self.jewelry_df.iterrows():
                feature_vector = [
                    row['weight'], row['size'], row['price'],
                    hash(row['metal']) % 1000,
                    hash(row['stone']) % 1000,
                    hash(row['category']) % 1000
                ]
                features.append(feature_vector)
            
            # Use KMeans for clustering similar jewelry
            self.jewelry_recommender = KMeans(n_clusters=min(20, len(features)), random_state=42)
            self.jewelry_recommender.fit(features)
            
        except Exception as e:
            logger.error(f"Error training jewelry recommender: {e}")
    
    def _train_diamond_recommender(self):
        """Train diamond recommendation model"""
        try:
            # Prepare features for diamond recommendation
            features = self.diamonds_df[['carat', 'depth', 'table', 'price', 'x', 'y', 'z']].fillna(0)
            
            # Use KMeans for clustering similar diamonds
            self.diamond_recommender = KMeans(n_clusters=min(15, len(features)), random_state=42)
            self.diamond_recommender.fit(features)
            
        except Exception as e:
            logger.error(f"Error training diamond recommender: {e}")
    
    def process_query(self, message: str) -> Dict[str, Any]:
        """Process user query with advanced understanding"""
        try:
            # Clean and analyze the message
            cleaned_message = self._clean_message(message)
            
            # Classify intent
            intent = self._classify_intent(cleaned_message)
            
            # Extract entities
            entities = self._extract_entities(cleaned_message)
            
            # Generate intelligent response based on intent and entities
            response = self._generate_intelligent_response(intent, entities, cleaned_message)
            
            return {
                'response': response,
                'intent': intent,
                'entities': entities,
                'confidence': 0.95,
                'source': 'advanced_ml',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                'response': "I apologize, but I'm having trouble processing your request. Could you please rephrase your question?",
                'intent': 'error',
                'entities': {},
                'confidence': 0.0,
                'source': 'error_fallback',
                'timestamp': datetime.now().isoformat()
            }
    
    def _clean_message(self, message: str) -> str:
        """Clean and normalize the message"""
        # Convert to lowercase
        cleaned = message.lower().strip()
        
        # Remove extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Expand contractions
        contractions = {
            "i'm": "i am", "you're": "you are", "it's": "it is",
            "that's": "that is", "what's": "what is", "there's": "there is",
            "can't": "cannot", "don't": "do not", "won't": "will not"
        }
        
        for contraction, expansion in contractions.items():
            cleaned = cleaned.replace(contraction, expansion)
        
        return cleaned
    
    def _classify_intent(self, message: str) -> str:
        """Classify the intent of the message"""
        try:
            # Use TF-IDF and trained classifier
            X = self.tfidf_vectorizer.transform([message])
            predicted_intent = self.intent_classifier.predict(X)[0]
            
            # Additional rule-based classification for edge cases
            if any(word in message for word in ['compare', 'vs', 'better', 'which']):
                return 'comparison'
            elif any(word in message for word in ['recommend', 'suggest', 'suits me']):
                return 'recommendation'
            elif any(word in message for word in ['price', 'cost', 'budget']):
                return 'pricing'
            
            return predicted_intent
            
        except Exception as e:
            logger.error(f"Error classifying intent: {e}")
            return 'general_inquiry'
    
    def _extract_entities(self, message: str) -> Dict[str, List[str]]:
        """Extract entities from the message"""
        entities = {
            'products': [],
            'materials': [],
            'gemstones': [],
            'price_range': [],
            'occasions': [],
            'preferences': []
        }
        
        # Product entities
        products = ['ring', 'necklace', 'earring', 'bracelet', 'engagement ring', 'wedding band']
        for product in products:
            if product in message:
                entities['products'].append(product)
        
        # Material entities
        materials = ['gold', 'silver', 'platinum', 'white gold', 'rose gold']
        for material in materials:
            if material in message:
                entities['materials'].append(material)
        
        # Gemstone entities
        gemstones = ['diamond', 'emerald', 'ruby', 'sapphire', 'pearl']
        for gemstone in gemstones:
            if gemstone in message:
                entities['gemstones'].append(gemstone)
        
        # Price range entities
        if re.search(r'\$?\d+k?', message):
            price_matches = re.findall(r'\$?(\d+)k?', message)
            entities['price_range'] = price_matches
        
        # Occasion entities
        occasions = ['wedding', 'engagement', 'anniversary', 'birthday', 'valentine']
        for occasion in occasions:
            if occasion in message:
                entities['occasions'].append(occasion)
        
        return entities
    
    def _generate_intelligent_response(self, intent: str, entities: Dict, message: str) -> str:
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
        """Handle comparison queries with intelligent analysis"""
        
        if 'suits me' in message or 'best for me' in message:
            return self._generate_personal_recommendation(entities, message)
        
        products = entities.get('products', [])
        materials = entities.get('materials', [])
        gemstones = entities.get('gemstones', [])
        
        if len(products) >= 2:
            return self._compare_products(products)
        elif len(materials) >= 2:
            return self._compare_materials(materials)
        elif len(gemstones) >= 2:
            return self._compare_gemstones(gemstones)
        else:
            return self._generate_general_comparison_advice()
    
    def _generate_personal_recommendation(self, entities: Dict, message: str) -> str:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Analyze user preferences from message
        if 'elegant' in message or 'classic' in message:
            recommendations.append("For an elegant, classic look, I'd recommend our platinum engagement rings with round brilliant diamonds. They offer timeless sophistication.")
        
        if 'modern' in message or 'contemporary' in message:
            recommendations.append("For a modern aesthetic, consider our rose gold pieces with emerald-cut stones or our geometric designs.")
        
        if 'budget' in message or 'affordable' in message:
            recommendations.append("For excellent value, our silver collections and smaller carat diamonds offer beautiful options without compromising quality.")
        
        if entities.get('occasions'):
            occasion = entities['occasions'][0]
            if occasion == 'engagement':
                recommendations.append("For engagements, round brilliant diamonds in white gold settings are most popular, offering maximum sparkle and timeless appeal.")
            elif occasion == 'wedding':
                recommendations.append("Wedding bands in matching metals to your engagement ring create a cohesive, elegant set.")
        
        if not recommendations:
            recommendations.append("To give you the best recommendation, I'd love to know more about your style preferences, budget range, and the occasion. Our bespoke consultation service can help create something perfect for you!")
        
        # Add data-driven insights
        if self.jewelry_df is not None:
            popular_items = self._get_popular_items()
            recommendations.append(f"Based on our collection data, {popular_items} are trending this season.")
        
        return " ".join(recommendations) + " Would you like to schedule a consultation to explore options that perfectly suit your style?"
    
    def _compare_products(self, products: List[str]) -> str:
        """Compare different product types"""
        comparison_data = {
            'ring': {
                'versatility': 'High - suitable for daily wear',
                'symbolism': 'Strong - represents commitment and love',
                'maintenance': 'Medium - requires regular cleaning'
            },
            'necklace': {
                'versatility': 'Very High - works with any outfit',
                'symbolism': 'Moderate - represents elegance',
                'maintenance': 'Low - easy to maintain'
            },
            'earring': {
                'versatility': 'High - complements face shape',
                'symbolism': 'Low - mainly aesthetic',
                'maintenance': 'Low - minimal care needed'
            },
            'bracelet': {
                'versatility': 'Medium - depends on style',
                'symbolism': 'Moderate - represents connection',
                'maintenance': 'Medium - regular cleaning needed'
            }
        }
        
        response = f"Comparing {' vs '.join(products)}:\n\n"
        
        for product in products:
            if product in comparison_data:
                data = comparison_data[product]
                response += f"**{product.title()}:**\n"
                response += f"• Versatility: {data['versatility']}\n"
                response += f"• Symbolism: {data['symbolism']}\n"
                response += f"• Maintenance: {data['maintenance']}\n\n"
        
        response += "The best choice depends on your personal style, lifestyle, and the occasion. Would you like specific recommendations based on your preferences?"
        
        return response
    
    def _compare_materials(self, materials: List[str]) -> str:
        """Compare different materials"""
        material_data = {
            'gold': {
                'durability': 'Excellent',
                'price': 'High',
                'maintenance': 'Low',
                'appearance': 'Warm, classic yellow tone'
            },
            'white gold': {
                'durability': 'Excellent',
                'price': 'High',
                'maintenance': 'Medium (needs rhodium re-plating)',
                'appearance': 'Cool, modern silver tone'
            },
            'rose gold': {
                'durability': 'Excellent',
                'price': 'High',
                'maintenance': 'Low',
                'appearance': 'Romantic, warm pink tone'
            },
            'platinum': {
                'durability': 'Outstanding',
                'price': 'Very High',
                'maintenance': 'Very Low',
                'appearance': 'Pure, naturally white'
            },
            'silver': {
                'durability': 'Good',
                'price': 'Low',
                'maintenance': 'High (tarnishes)',
                'appearance': 'Bright, reflective white'
            }
        }
        
        response = f"Material Comparison - {' vs '.join(materials)}:\n\n"
        
        for material in materials:
            if material in material_data:
                data = material_data[material]
                response += f"**{material.replace('_', ' ').title()}:**\n"
                response += f"• Durability: {data['durability']}\n"
                response += f"• Price Range: {data['price']}\n"
                response += f"• Maintenance: {data['maintenance']}\n"
                response += f"• Appearance: {data['appearance']}\n\n"
        
        response += "Consider your budget, skin tone, and lifestyle when choosing. Platinum offers the best durability, while gold options provide variety in appearance."
        
        return response
    
    def _compare_gemstones(self, gemstones: List[str]) -> str:
        """Compare different gemstones"""
        gemstone_data = {
            'diamond': {
                'hardness': '10 (Hardest)',
                'brilliance': 'Exceptional',
                'rarity': 'Moderate',
                'symbolism': 'Eternal love, strength'
            },
            'emerald': {
                'hardness': '7.5-8',
                'brilliance': 'Good',
                'rarity': 'High',
                'symbolism': 'Growth, harmony, wisdom'
            },
            'ruby': {
                'hardness': '9',
                'brilliance': 'Excellent',
                'rarity': 'Very High',
                'symbolism': 'Passion, protection, prosperity'
            },
            'sapphire': {
                'hardness': '9',
                'brilliance': 'Excellent',
                'rarity': 'High',
                'symbolism': 'Truth, sincerity, faithfulness'
            },
            'pearl': {
                'hardness': '2.5-4.5',
                'brilliance': 'Lustrous',
                'rarity': 'Moderate',
                'symbolism': 'Purity, wisdom, integrity'
            }
        }
        
        response = f"Gemstone Comparison - {' vs '.join(gemstones)}:\n\n"
        
        for gemstone in gemstones:
            if gemstone in gemstone_data:
                data = gemstone_data[gemstone]
                response += f"**{gemstone.title()}:**\n"
                response += f"• Hardness: {data['hardness']} (Mohs scale)\n"
                response += f"• Brilliance: {data['brilliance']}\n"
                response += f"• Rarity: {data['rarity']}\n"
                response += f"• Symbolism: {data['symbolism']}\n\n"
        
        response += "Diamond offers maximum durability and brilliance, while colored stones add personal meaning and unique beauty to your jewelry."
        
        return response
    
    def _handle_recommendation_query(self, entities: Dict, message: str) -> str:
        """Handle recommendation queries with ML-powered suggestions"""
        recommendations = []
        
        # Analyze budget from message
        budget_range = self._extract_budget_range(message)
        
        # Use ML models for recommendations if available
        if self.jewelry_df is not None:
            ml_recommendations = self._get_ml_recommendations(entities, budget_range)
            recommendations.extend(ml_recommendations)
        
        # Add personalized recommendations based on entities
        if entities.get('occasions'):
            occasion_recs = self._get_occasion_recommendations(entities['occasions'][0])
            recommendations.extend(occasion_recs)
        
        if not recommendations:
            recommendations = [
                "I'd love to help you find the perfect piece! Here are some popular recommendations:",
                "• **Engagement Rings**: Classic solitaire diamonds in platinum or white gold",
                "• **Wedding Bands**: Matching metal bands with subtle diamond accents",
                "• **Necklaces**: Delicate gold chains with pendant options",
                "• **Earrings**: Diamond studs or elegant drop styles"
            ]
        
        recommendations.append("For personalized recommendations, I'd suggest booking a consultation where we can discuss your style, preferences, and budget in detail.")
        
        return "\n".join(recommendations)
    
    def _extract_budget_range(self, message: str) -> Tuple[int, int]:
        """Extract budget range from message"""
        # Look for price patterns
        price_patterns = [
            r'\$(\d+)k?(?:\s*-\s*\$?(\d+)k?)?',
            r'under\s+\$?(\d+)k?',
            r'below\s+\$?(\d+)k?',
            r'around\s+\$?(\d+)k?'
        ]
        
        for pattern in price_patterns:
            matches = re.search(pattern, message.lower())
            if matches:
                min_price = int(matches.group(1)) * (1000 if 'k' in matches.group(0) else 1)
                max_price = min_price * 2 if not matches.group(2) else int(matches.group(2)) * (1000 if 'k' in matches.group(0) else 1)
                return (min_price, max_price)
        
        # Default budget ranges based on keywords
        if 'budget' in message or 'affordable' in message:
            return (500, 5000)
        elif 'luxury' in message or 'premium' in message:
            return (15000, 50000)
        else:
            return (2000, 15000)
    
    def _get_ml_recommendations(self, entities: Dict, budget_range: Tuple[int, int]) -> List[str]:
        """Get ML-powered recommendations"""
        recommendations = []
        
        if self.jewelry_df is not None and len(self.jewelry_df) > 0:
            # Filter by budget
            filtered_df = self.jewelry_df[
                (self.jewelry_df['price'] >= budget_range[0]) & 
                (self.jewelry_df['price'] <= budget_range[1])
            ]
            
            # Filter by entities
            if entities.get('products'):
                product_filter = entities['products'][0].replace(' ', '_')
                filtered_df = filtered_df[filtered_df['category'].str.contains(product_filter, case=False, na=False)]
            
            if entities.get('materials'):
                material_filter = entities['materials'][0]
                filtered_df = filtered_df[filtered_df['metal'].str.contains(material_filter, case=False, na=False)]
            
            # Get top recommendations
            if not filtered_df.empty:
                top_items = filtered_df.nsmallest(3, 'price')
                for _, item in top_items.iterrows():
                    rec = f"• **{item['category'].title()} in {item['metal'].title()}** with {item['stone']} - ${item['price']:,.0f}"
                    recommendations.append(rec)
        
        return recommendations
    
    def _get_occasion_recommendations(self, occasion: str) -> List[str]:
        """Get occasion-specific recommendations"""
        occasion_map = {
            'engagement': [
                "• **Classic Solitaire**: Timeless round diamond in platinum setting",
                "• **Vintage Inspired**: Art deco designs with intricate details",
                "• **Modern Elegance**: Princess cut diamonds in white gold"
            ],
            'wedding': [
                "• **Matching Bands**: Complement your engagement ring perfectly",
                "• **Diamond Eternity**: Continuous sparkle all around",
                "• **Classic Plain**: Timeless and versatile for daily wear"
            ],
            'anniversary': [
                "• **Eternity Rings**: Celebrate your continuing journey",
                "• **Pendant Necklaces**: Personal and meaningful",
                "• **Tennis Bracelets**: Elegant and luxurious"
            ]
        }
        
        return occasion_map.get(occasion, [])
    
    def _handle_product_inquiry(self, entities: Dict, message: str) -> str:
        """Handle product inquiry with dataset insights"""
        response_parts = []
        
        if entities.get('products'):
            product = entities['products'][0]
            response_parts.append(f"I'd be happy to help you with {product}s!")
            
            # Add dataset-driven insights
            if self.jewelry_df is not None:
                product_data = self._get_product_insights(product)
                response_parts.extend(product_data)
        
        # Add general product information
        response_parts.extend([
            "\n**Our Collections Include:**",
            "• **Engagement Rings**: Classic and contemporary designs",
            "• **Wedding Bands**: Perfect matches for your engagement ring",
            "• **Necklaces**: From delicate chains to statement pieces",
            "• **Earrings**: Studs, hoops, and elegant drops",
            "• **Bracelets**: Tennis, charm, and bangle styles",
            "\nWould you like to explore any specific style or see our current collections?"
        ])
        
        return "\n".join(response_parts)
    
    def _get_product_insights(self, product: str) -> List[str]:
        """Get insights about specific product from dataset"""
        insights = []
        
        if self.jewelry_df is not None:
            # Filter for the product
            product_df = self.jewelry_df[self.jewelry_df['category'].str.contains(product, case=False, na=False)]
            
            if not product_df.empty:
                # Price insights
                avg_price = product_df['price'].mean()
                price_range = (product_df['price'].min(), product_df['price'].max())
                insights.append(f"\n**{product.title()} Insights from our collection:**")
                insights.append(f"• Average price: ${avg_price:,.0f}")
                insights.append(f"• Price range: ${price_range[0]:,.0f} - ${price_range[1]:,.0f}")
                
                # Popular materials
                popular_materials = product_df['metal'].value_counts().head(3)
                materials_text = ", ".join([f"{mat} ({count} pieces)" for mat, count in popular_materials.items()])
                insights.append(f"• Popular materials: {materials_text}")
                
                # Popular stones
                popular_stones = product_df['stone'].value_counts().head(3)
                stones_text = ", ".join([f"{stone} ({count} pieces)" for stone, count in popular_stones.items()])
                insights.append(f"• Popular stones: {stones_text}")
        
        return insights
    
    def _handle_pricing_query(self, entities: Dict, message: str) -> str:
        """Handle pricing queries with detailed information"""
        response_parts = ["I'll help you understand our pricing structure:"]
        
        # Add dataset-driven pricing insights
        if self.jewelry_df is not None:
            pricing_insights = self._get_pricing_insights()
            response_parts.extend(pricing_insights)
        
        # Add diamond pricing if relevant
        if 'diamond' in message and self.diamonds_df is not None:
            diamond_pricing = self._get_diamond_pricing_insights()
            response_parts.extend(diamond_pricing)
        
        response_parts.extend([
            "\n**Pricing Factors:**",
            "• Material quality and type",
            "• Gemstone grade and size",
            "• Craftsmanship complexity",
            "• Brand and design exclusivity",
            "\nFor accurate pricing on specific pieces, I recommend scheduling a consultation or browsing our collections online."
        ])
        
        return "\n".join(response_parts)
    
    def _get_pricing_insights(self) -> List[str]:
        """Get pricing insights from jewelry dataset"""
        insights = []
        
        if self.jewelry_df is not None and len(self.jewelry_df) > 0:
            insights.append("\n**Our Collection Pricing Overview:**")
            
            # Price by category
            price_by_category = self.jewelry_df.groupby('category')['price'].agg(['mean', 'min', 'max'])
            for category, row in price_by_category.iterrows():
                insights.append(f"• **{category.title()}s**: ${row['min']:,.0f} - ${row['max']:,.0f} (avg: ${row['mean']:,.0f})")
            
            # Price by material
            price_by_material = self.jewelry_df.groupby('metal')['price'].mean().sort_values(ascending=False)
            insights.append(f"\n**By Material** (average prices):")
            for material, avg_price in price_by_material.head(5).items():
                insights.append(f"• {material.title()}: ${avg_price:,.0f}")
        
        return insights
    
    def _get_diamond_pricing_insights(self) -> List[str]:
        """Get diamond pricing insights"""
        insights = []
        
        if self.diamonds_df is not None and len(self.diamonds_df) > 0:
            insights.append("\n**Diamond Pricing Insights:**")
            
            # Price by carat range
            carat_ranges = [(0, 0.5), (0.5, 1.0), (1.0, 2.0), (2.0, float('inf'))]
            range_labels = ["Under 0.5ct", "0.5-1.0ct", "1.0-2.0ct", "Over 2.0ct"]
            
            for (min_carat, max_carat), label in zip(carat_ranges, range_labels):
                if max_carat == float('inf'):
                    filtered = self.diamonds_df[self.diamonds_df['carat'] >= min_carat]
                else:
                    filtered = self.diamonds_df[(self.diamonds_df['carat'] >= min_carat) & (self.diamonds_df['carat'] < max_carat)]
                
                if not filtered.empty:
                    avg_price = filtered['price'].mean()
                    insights.append(f"• **{label}**: Average ${avg_price:,.0f}")
            
            # Price per carat insights
            avg_price_per_carat = (self.diamonds_df['price'] / self.diamonds_df['carat']).mean()
            insights.append(f"• **Average price per carat**: ${avg_price_per_carat:,.0f}")
        
        return insights
    
    def _handle_technical_query(self, entities: Dict, message: str) -> str:
        """Handle technical queries about jewelry and diamonds"""
        response_parts = []
        
        if 'diamond' in message or '4c' in message:
            response_parts.extend([
                "**Diamond Quality - The 4Cs:**",
                "",
                "**Cut**: Determines brilliance and sparkle",
                "• Excellent/Ideal: Maximum light return",
                "• Very Good: High light return",
                "• Good: Good light return",
                "",
                "**Color**: Graded D (colorless) to Z (light yellow)",
                "• D-F: Colorless (most valuable)",
                "• G-J: Near colorless (excellent value)",
                "• K+: Slight color (budget-friendly)",
                "",
                "**Clarity**: Measures internal inclusions",
                "• FL/IF: Flawless (rare)",
                "• VVS1/VVS2: Very very slightly included",
                "• VS1/VS2: Very slightly included (excellent choice)",
                "• SI1/SI2: Slightly included (good value)",
                "",
                "**Carat**: Weight of the diamond",
                "• 1 carat = 200 milligrams",
                "• Price increases exponentially with size"
            ])
            
            # Add dataset insights if available
            if self.diamonds_df is not None:
                diamond_insights = self._get_diamond_technical_insights()
                response_parts.extend(diamond_insights)
        
        response_parts.append("\nWould you like detailed information about any specific aspect of diamond grading?")
        
        return "\n".join(response_parts)
    
    def _get_diamond_technical_insights(self) -> List[str]:
        """Get technical insights from diamond dataset"""
        insights = []
        
        if self.diamonds_df is not None and len(self.diamonds_df) > 0:
            insights.append("\n**Insights from Our Diamond Collection:**")
            
            # Cut distribution
            cut_dist = self.diamonds_df['cut'].value_counts()
            insights.append(f"• Most common cut: {cut_dist.index[0]} ({cut_dist.iloc[0]} diamonds)")
            
            # Color distribution
            color_dist = self.diamonds_df['color'].value_counts()
            insights.append(f"• Most common color grade: {color_dist.index[0]} ({color_dist.iloc[0]} diamonds)")
            
            # Clarity distribution
            clarity_dist = self.diamonds_df['clarity'].value_counts()
            insights.append(f"• Most common clarity: {clarity_dist.index[0]} ({clarity_dist.iloc[0]} diamonds)")
            
            # Size insights
            avg_carat = self.diamonds_df['carat'].mean()
            insights.append(f"• Average carat weight: {avg_carat:.2f}ct")
            
            # Quality correlation
            if 'quality_score' in self.diamonds_df.columns:
                high_quality = self.diamonds_df[self.diamonds_df['quality_score'] >= 4.0]
                insights.append(f"• {len(high_quality)} diamonds with quality score 4.0+ out of 5.0")
        
        return insights
    
    def _handle_services_query(self, entities: Dict, message: str) -> str:
        """Handle service-related queries"""
        services_info = {
            'bespoke': "Our bespoke design service creates one-of-a-kind pieces tailored to your vision. The process includes initial consultation, design sketches, 3D modeling, and expert craftsmanship.",
            'custom': "Custom jewelry allows you to personalize existing designs or create something entirely new. We work with you through every step of the creation process.",
            'resize': "Professional resizing services for rings and bracelets. Most pieces can be adjusted up or down 2-3 sizes while maintaining structural integrity.",
            'repair': "Expert repair services for all types of jewelry including stone replacement, prong repair, chain fixing, and restoration of vintage pieces.",
            'clean': "Professional cleaning and maintenance services to keep your jewelry sparkling. Includes ultrasonic cleaning, polishing, and inspection.",
            'appointment': "Schedule a personal consultation with our jewelry experts. Available for design discussions, fittings, maintenance, and collection viewing."
        }
        
        response_parts = ["**Our Jewelry Services:**"]
        
        # Add specific service information based on query
        found_services = []
        for service, description in services_info.items():
            if service in message:
                found_services.append(f"\n**{service.title()}**: {description}")
        
        if found_services:
            response_parts.extend(found_services)
        else:
            # Add all services if none specifically mentioned
            for service, description in services_info.items():
                response_parts.append(f"\n**{service.title()}**: {description}")
        
        response_parts.extend([
            "\n**Why Choose Our Services:**",
            "• Expert craftsmen with decades of experience",
            "• High-quality materials and ethical sourcing",
            "• Lifetime maintenance and care guidance",
            "• Satisfaction guarantee on all work",
            "\nWould you like to schedule a consultation or learn more about any specific service?"
        ])
        
        return "\n".join(response_parts)
    
    def _handle_education_query(self, entities: Dict, message: str) -> str:
        """Handle educational queries about jewelry"""
        education_topics = {
            'care': [
                "**Jewelry Care Guide:**",
                "",
                "**Daily Care:**",
                "• Remove jewelry before exercising, swimming, or cleaning",
                "• Store pieces separately to prevent scratching",
                "• Clean regularly with appropriate methods",
                "",
                "**Cleaning Methods:**",
                "• Diamonds: Gentle brush with warm soapy water",
                "• Pearls: Soft damp cloth only (no chemicals)",
                "• Gold: Mild soap and water, professional cleaning annually",
                "• Silver: Anti-tarnish cloths and proper storage"
            ],
            'sizing': [
                "**Ring Sizing Guide:**",
                "",
                "**How to Measure:**",
                "• Best time: End of day when fingers are largest",
                "• Use a ring sizer or measure existing ring",
                "• Consider knuckle size for proper fit",
                "",
                "**Size Factors:**",
                "• Temperature affects finger size",
                "• Wide bands feel tighter than thin bands",
                "• Comfort fit bands require smaller size"
            ],
            'gemstone': [
                "**Gemstone Education:**",
                "",
                "**Natural vs Synthetic:**",
                "• Natural: Formed in earth over millions of years",
                "• Synthetic: Lab-created with same properties",
                "• Both have identical chemical composition",
                "",
                "**Treatment Information:**",
                "• Heat treatment: Enhances color and clarity",
                "• Fracture filling: Improves clarity appearance",
                "• Always disclosed for transparency"
            ]
        }
        
        # Determine which topic to address
        topic = None
        for key in education_topics.keys():
            if key in message:
                topic = key
                break
        
        if topic:
            return "\n".join(education_topics[topic])
        else:
            # General jewelry education
            return "\n".join([
                "**Jewelry Education Topics:**",
                "",
                "**Care & Maintenance**: How to keep your jewelry beautiful",
                "**Ring Sizing**: Finding the perfect fit",
                "**Gemstone Knowledge**: Understanding different stones",
                "**Metal Properties**: Gold, platinum, and silver characteristics",
                "**Diamond Grading**: The 4Cs explained in detail",
                "",
                "What specific topic would you like to learn about?"
            ])
    
    def _handle_general_query(self, entities: Dict, message: str) -> str:
        """Handle general queries with comprehensive information"""
        return """Welcome to Ornament Tech! I'm here to help you discover the perfect jewelry.

**I can assist you with:**
• Product recommendations based on your preferences
• Detailed comparisons between different options
• Pricing information and budget guidance
• Technical details about diamonds and gemstones
• Information about our services and processes
• Educational content about jewelry care and selection

**Our Specialties:**
• Engagement rings and wedding bands
• Custom and bespoke jewelry design
• Certified diamonds and precious gemstones
• Expert craftsmanship and lifetime service

**Popular Collections:**
• Classic solitaire engagement rings
• Vintage-inspired designs
• Modern geometric pieces
• Luxury statement jewelry

What specific information can I help you find today? Feel free to ask about products, pricing, services, or anything else jewelry-related!"""
    
    def _get_popular_items(self) -> str:
        """Get popular items from dataset"""
        if self.jewelry_df is not None and len(self.jewelry_df) > 0:
            # Find most common combinations
            popular_combo = self.jewelry_df.groupby(['category', 'metal']).size().nlargest(1)
            if not popular_combo.empty:
                category, metal = popular_combo.index[0]
                return f"{metal} {category}s"
        
        return "classic diamond engagement rings"
    
    def _generate_general_comparison_advice(self) -> str:
        """Generate general comparison advice"""
        return """When comparing jewelry options, consider these key factors:

**Quality Factors:**
• Material purity and durability
• Gemstone grade and certification
• Craftsmanship and attention to detail
• Brand reputation and warranty

**Personal Factors:**
• Your lifestyle and daily activities
• Skin tone and personal style
• Budget and long-term value
• Occasion and symbolic meaning

**Practical Considerations:**
• Maintenance requirements
• Sizing and fit options
• Matching with existing pieces
• Resale value potential

Would you like specific comparisons between particular items or materials? I can provide detailed analysis based on your preferences."""

# Initialize the bot
bot = AdvancedJewelryBot()

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({
                'response': 'Please provide a message.',
                'error': 'Empty message'
            }), 400
        
        # Process the query with advanced ML
        result = bot.process_query(message)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({
            'response': 'I apologize for the technical issue. Please try again.',
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
            'diamond_items': len(bot.diamonds_df) if bot.diamonds_df is not None else 0
        }
    })

@app.route('/analytics', methods=['GET'])
def analytics():
    """Analytics endpoint for dataset insights"""
    try:
        analytics_data = {
            'dataset_summary': {},
            'popular_items': {},
            'price_insights': {},
            'recommendations': []
        }
        
        if bot.jewelry_df is not None:
            analytics_data['dataset_summary']['jewelry'] = {
                'total_items': len(bot.jewelry_df),
                'categories': bot.jewelry_df['category'].nunique(),
                'avg_price': float(bot.jewelry_df['price'].mean()),
                'price_range': [float(bot.jewelry_df['price'].min()), float(bot.jewelry_df['price'].max())]
            }
            
            analytics_data['popular_items']['jewelry'] = {
                'categories': bot.jewelry_df['category'].value_counts().head(5).to_dict(),
                'materials': bot.jewelry_df['metal'].value_counts().head(5).to_dict(),
                'stones': bot.jewelry_df['stone'].value_counts().head(5).to_dict()
            }
        
        if bot.diamonds_df is not None:
            analytics_data['dataset_summary']['diamonds'] = {
                'total_items': len(bot.diamonds_df),
                'avg_carat': float(bot.diamonds_df['carat'].mean()),
                'avg_price': float(bot.diamonds_df['price'].mean()),
                'price_range': [float(bot.diamonds_df['price'].min()), float(bot.diamonds_df['price'].max())]
            }
            
            analytics_data['popular_items']['diamonds'] = {
                'cuts': bot.diamonds_df['cut'].value_counts().head(5).to_dict(),
                'colors': bot.diamonds_df['color'].value_counts().head(5).to_dict(),
                'clarities': bot.diamonds_df['clarity'].value_counts().head(5).to_dict()
            }
        
        return jsonify(analytics_data)
        
    except Exception as e:
        logger.error(f"Error in analytics endpoint: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    logger.info(f"🚀 Starting {bot.app_name} v{bot.version}")
    logger.info("🔗 Endpoints available:")
    logger.info("   POST /chat - Main chat interface")
    logger.info("   GET /health - Health check")
    logger.info("   GET /analytics - Dataset analytics")
    
    app.run(host='0.0.0.0', port=5000, debug=False)