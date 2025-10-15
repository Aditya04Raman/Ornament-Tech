"""
Enhanced Jewelry Chatbot with Real Dataset Integration
"""
import json
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import re
from datetime import datetime

class EnhancedJewelryChatbot:
    def __init__(self):
        """
        Initialize enhanced chatbot with dataset-trained models
        """
        self.intent_model = None
        self.price_model = None
        self.vectorizer = None
        self.label_encoder = None
        self.price_scaler = None
        
        # Dataset storage
        self.diamonds_data = None
        self.jewelry_data = None
        self.qa_pairs = None
        
        # Response data
        self.dataset_responses = {}
        
    def load_models(self):
        """
        Load all trained models and datasets
        """
        try:
            model_dir = os.path.join(os.path.dirname(__file__), 'models')
            
            # Load enhanced models
            if os.path.exists(os.path.join(model_dir, 'enhanced_intent_model.h5')):
                self.intent_model = tf.keras.models.load_model(os.path.join(model_dir, 'enhanced_intent_model.h5'))
                print("✓ Enhanced intent model loaded")
            
            if os.path.exists(os.path.join(model_dir, 'price_prediction_model.h5')):
                self.price_model = tf.keras.models.load_model(os.path.join(model_dir, 'price_prediction_model.h5'))
                print("✓ Price prediction model loaded")
            
            # Load preprocessors
            with open(os.path.join(model_dir, 'enhanced_vectorizer.pkl'), 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            with open(os.path.join(model_dir, 'enhanced_label_encoder.pkl'), 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            if os.path.exists(os.path.join(model_dir, 'price_scaler.pkl')):
                with open(os.path.join(model_dir, 'price_scaler.pkl'), 'rb') as f:
                    self.price_scaler = pickle.load(f)
            
            # Load datasets
            if os.path.exists(os.path.join(model_dir, 'diamonds_dataset.csv')):
                self.diamonds_data = pd.read_csv(os.path.join(model_dir, 'diamonds_dataset.csv'))
                print(f"✓ Diamonds dataset loaded: {len(self.diamonds_data)} samples")
            
            if os.path.exists(os.path.join(model_dir, 'jewelry_dataset.csv')):
                self.jewelry_data = pd.read_csv(os.path.join(model_dir, 'jewelry_dataset.csv'))
                print(f"✓ Jewelry dataset loaded: {len(self.jewelry_data)} samples")
            
            # Load Q&A pairs
            if os.path.exists(os.path.join(model_dir, 'dataset_qa_pairs.json')):
                with open(os.path.join(model_dir, 'dataset_qa_pairs.json'), 'r') as f:
                    self.qa_pairs = json.load(f)
                print(f"✓ Dataset Q&A pairs loaded: {len(self.qa_pairs)}")
            
            return True
            
        except Exception as e:
            print(f"Error loading enhanced models: {e}")
            return False
    
    def predict_diamond_price(self, carat, cut, color, clarity, depth=60, table=60, x=5, y=5, z=3):
        """
        Predict diamond price using trained ML model
        """
        if self.price_model is None or self.price_scaler is None:
            return None
        
        try:
            # Encode categorical variables (simplified mapping)
            cut_mapping = {'Fair': 0, 'Good': 1, 'Very Good': 2, 'Premium': 3, 'Ideal': 4}
            color_mapping = {'J': 0, 'I': 1, 'H': 2, 'G': 3, 'F': 4, 'E': 5, 'D': 6}
            clarity_mapping = {'SI2': 0, 'SI1': 1, 'VS2': 2, 'VS1': 3, 'VVS2': 4, 'VVS1': 5, 'IF': 6, 'FL': 7}
            
            cut_encoded = cut_mapping.get(cut, 2)
            color_encoded = color_mapping.get(color, 3)
            clarity_encoded = clarity_mapping.get(clarity, 2)
            
            # Prepare features
            features = np.array([[carat, cut_encoded, color_encoded, clarity_encoded, depth, table, x, y, z]])
            features_scaled = self.price_scaler.transform(features)
            
            # Predict
            prediction = self.price_model.predict(features_scaled)[0][0]
            return max(100, prediction)  # Minimum price
            
        except Exception as e:
            print(f"Error predicting price: {e}")
            return None
    
    def get_jewelry_recommendations(self, category, budget=None, metal=None):
        """
        Get jewelry recommendations from dataset
        """
        if self.jewelry_data is None:
            return []
        
        try:
            # Filter by category
            filtered_data = self.jewelry_data[self.jewelry_data['category'] == category.lower()]
            
            # Apply filters
            if budget:
                filtered_data = filtered_data[filtered_data['price'] <= budget]
            
            if metal:
                filtered_data = filtered_data[filtered_data['metal'].str.contains(metal.lower(), na=False)]
            
            # Get top recommendations
            recommendations = filtered_data.nlargest(5, 'price')[['type', 'metal', 'stone', 'price']].to_dict('records')
            return recommendations
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
    
    def get_dataset_statistics(self, query):
        """
        Get statistical insights from datasets based on query
        """
        query_lower = query.lower()
        
        try:
            if 'diamond' in query_lower and self.diamonds_data is not None:
                stats = {
                    'average_price': f"${self.diamonds_data['price'].mean():.0f}",
                    'price_range': f"${self.diamonds_data['price'].min():.0f} - ${self.diamonds_data['price'].max():.0f}",
                    'most_common_cut': self.diamonds_data['cut'].mode().iloc[0],
                    'average_carat': f"{self.diamonds_data['carat'].mean():.2f}ct"
                }
                return stats
            
            elif any(word in query_lower for word in ['ring', 'necklace', 'earring', 'bracelet']) and self.jewelry_data is not None:
                category = None
                for cat in ['ring', 'necklace', 'earrings', 'bracelet']:
                    if cat in query_lower:
                        category = cat
                        break
                
                if category:
                    cat_data = self.jewelry_data[self.jewelry_data['category'] == category]
                    if len(cat_data) > 0:
                        stats = {
                            'count': len(cat_data),
                            'average_price': f"${cat_data['price'].mean():.0f}",
                            'price_range': f"${cat_data['price'].min():.0f} - ${cat_data['price'].max():.0f}",
                            'popular_metal': cat_data['metal'].mode().iloc[0] if len(cat_data) > 0 else 'gold'
                        }
                        return stats
            
            return None
            
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return None
    
    def classify_intent(self, user_input):
        """
        Enhanced intent classification using dataset-trained model
        """
        if self.intent_model is None or self.vectorizer is None:
            return 'general_info'
        
        try:
            # Preprocess input
            processed_input = self.preprocess_text(user_input)
            
            # Vectorize
            input_vector = self.vectorizer.transform([processed_input])
            
            # Predict intent
            intent_probs = self.intent_model.predict(input_vector.toarray())
            intent_idx = np.argmax(intent_probs)
            intent = self.label_encoder.inverse_transform([intent_idx])[0]
            confidence = intent_probs[0][intent_idx]
            
            return intent, confidence
            
        except Exception as e:
            print(f"Error classifying intent: {e}")
            return 'general_info', 0.5
    
    def find_best_response(self, user_input, intent):
        """
        Find best response using dataset-derived Q&A and ML insights
        """
        user_input_lower = user_input.lower()
        
        # Handle price prediction requests
        if intent == 'pricing' and 'diamond' in user_input_lower:
            return self.handle_diamond_price_query(user_input)
        
        # Handle recommendation requests
        if intent in ['ring_info', 'jewelry_info']:
            return self.handle_recommendation_query(user_input, intent)
        
        # Handle statistical queries
        if any(word in user_input_lower for word in ['average', 'typical', 'most', 'statistics']):
            stats = self.get_dataset_statistics(user_input)
            if stats:
                return self.format_statistics_response(stats, user_input)
        
        # Find similar Q&A from dataset
        if self.qa_pairs:
            best_match = self.find_similar_qa(user_input)
            if best_match:
                return best_match[1]  # Return answer
        
        # Fallback to general responses
        return self.get_fallback_response(intent)
    
    def handle_diamond_price_query(self, user_input):
        """
        Handle diamond price prediction queries
        """
        # Extract diamond characteristics from query (simplified)
        carat = 1.0  # Default
        cut = 'Very Good'
        color = 'G'
        clarity = 'VS1'
        
        # Simple keyword extraction
        if '2 carat' in user_input.lower() or '2ct' in user_input.lower():
            carat = 2.0
        elif '0.5 carat' in user_input.lower() or '0.5ct' in user_input.lower():
            carat = 0.5
        
        if 'ideal' in user_input.lower():
            cut = 'Ideal'
        elif 'premium' in user_input.lower():
            cut = 'Premium'
        
        predicted_price = self.predict_diamond_price(carat, cut, color, clarity)
        
        if predicted_price:
            return f"Based on our ML model trained on diamond data, a {carat}ct {cut} cut diamond with {color} color and {clarity} clarity would be approximately ${predicted_price:.0f}. Prices vary based on specific characteristics and market conditions. Would you like to schedule a consultation to see actual diamonds?"
        else:
            return "I'd be happy to help estimate diamond prices. Could you provide details about carat weight, cut, color, and clarity? Or visit our store for accurate pricing on specific diamonds."
    
    def handle_recommendation_query(self, user_input, intent):
        """
        Handle jewelry recommendation queries
        """
        category = 'ring'  # Default
        budget = None
        metal = None
        
        # Extract category
        if 'necklace' in user_input.lower():
            category = 'necklace'
        elif 'earring' in user_input.lower():
            category = 'earrings'
        elif 'bracelet' in user_input.lower():
            category = 'bracelet'
        
        # Extract budget (simplified)
        import re
        budget_match = re.search(r'(\$|£)(\d+)', user_input)
        if budget_match:
            budget = int(budget_match.group(2))
        
        # Extract metal preference
        metals = ['gold', 'platinum', 'silver']
        for m in metals:
            if m in user_input.lower():
                metal = m
                break
        
        recommendations = self.get_jewelry_recommendations(category, budget, metal)
        
        if recommendations:
            response = f"Based on our jewelry dataset, here are some {category} recommendations"
            if budget:
                response += f" under ${budget}"
            response += ":\n\n"
            
            for i, rec in enumerate(recommendations[:3], 1):
                response += f"{i}. {rec['type'].title()} {category} in {rec['metal']} with {rec['stone']} - ${rec['price']:.0f}\n"
            
            response += "\nWould you like to see these pieces in person? I can schedule a consultation for you."
            return response
        else:
            return f"I'd be happy to help you find the perfect {category}. Could you tell me more about your style preferences and budget?"
    
    def find_similar_qa(self, user_input):
        """
        Find most similar Q&A pair from dataset
        """
        if not self.qa_pairs or not self.vectorizer:
            return None
        
        try:
            # Vectorize user input
            user_vector = self.vectorizer.transform([self.preprocess_text(user_input)])
            
            # Vectorize all questions
            questions = [qa[0] for qa in self.qa_pairs]
            question_vectors = self.vectorizer.transform([self.preprocess_text(q) for q in questions])
            
            # Calculate similarities
            similarities = cosine_similarity(user_vector, question_vectors)[0]
            
            # Find best match
            best_idx = np.argmax(similarities)
            best_score = similarities[best_idx]
            
            if best_score > 0.3:  # Threshold for similarity
                return self.qa_pairs[best_idx]
            
            return None
            
        except Exception as e:
            print(f"Error finding similar Q&A: {e}")
            return None
    
    def format_statistics_response(self, stats, query):
        """
        Format statistical response
        """
        if 'diamond' in query.lower():
            return f"Based on our diamond dataset analysis:\n- Average price: {stats['average_price']}\n- Price range: {stats['price_range']}\n- Most popular cut: {stats['most_common_cut']}\n- Average carat: {stats['average_carat']}\n\nThese are based on market data. Actual prices depend on specific characteristics and current market conditions."
        else:
            category = 'jewelry'
            for cat in ['ring', 'necklace', 'earrings', 'bracelet']:
                if cat in query.lower():
                    category = cat
                    break
            
            return f"From our {category} analysis:\n- Items available: {stats.get('count', 'Many')}\n- Average price: {stats['average_price']}\n- Price range: {stats['price_range']}\n- Popular metal: {stats['popular_metal']}\n\nWould you like to see specific pieces in these ranges?"
    
    def get_fallback_response(self, intent):
        """
        Fallback responses for different intents
        """
        fallbacks = {
            'pricing': "I'd be happy to help with pricing information. Our pieces range from affordable to luxury options. Could you tell me what type of jewelry you're interested in?",
            'diamond_info': "Diamonds are graded on the 4Cs: Carat, Cut, Color, and Clarity. Each affects the beauty and value. Would you like specific information about any of these?",
            'ring_info': "We offer a wide range of rings including engagement, wedding, and fashion rings. What style are you looking for?",
            'jewelry_info': "Our collection includes rings, necklaces, earrings, and bracelets in various metals and styles. What catches your interest?",
            'care': "Proper jewelry care extends its life and beauty. Clean regularly, store safely, and have professional maintenance. What specific care question do you have?",
            'custom_design': "We specialize in bespoke jewelry design. Our process takes 4-8 weeks from consultation to completion. Would you like to start with a consultation?",
            'general_info': "I'm here to help with all your jewelry questions. Feel free to ask about our products, services, or anything jewelry-related!"
        }
        
        return fallbacks.get(intent, fallbacks['general_info'])
    
    def preprocess_text(self, text):
        """
        Preprocess text for ML models
        """
        if not isinstance(text, str):
            return ""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        text = ' '.join(text.split())
        return text
    
    def generate_response(self, user_input):
        """
        Main response generation using enhanced ML pipeline
        """
        try:
            # Classify intent
            intent_result = self.classify_intent(user_input)
            if isinstance(intent_result, tuple):
                intent, confidence = intent_result
            else:
                intent = intent_result
                confidence = 0.7
            
            # Generate response based on intent and datasets
            response = self.find_best_response(user_input, intent)
            
            return {
                'response': response,
                'intent': intent,
                'confidence': float(confidence),
                'source': 'enhanced_ml_model',
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return {
                'response': "I apologize, but I'm having trouble processing your request right now. Please try again or contact our team directly.",
                'intent': 'error',
                'confidence': 0.0,
                'source': 'error_handler',
                'timestamp': datetime.now().isoformat()
            }