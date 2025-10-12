import numpy as np
import tensorflow as tf
import pickle
import json
import os
import re
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime

class JewelryChatbot:
    def __init__(self):
        """
        Initialize the jewelry chatbot with trained models
        """
        self.intent_model = None
        self.vectorizer = None
        self.label_encoder = None
        self.response_data = None
        self.metadata = None
        self.confidence_threshold = 0.6
        self.similarity_threshold = 0.3
        
    def load_models(self):
        """
        Load all trained models and preprocessors
        """
        try:
            model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
            
            # Load intent model
            intent_model_path = os.path.join(model_dir, 'intent_model.h5')
            self.intent_model = tf.keras.models.load_model(intent_model_path)
            
            # Load vectorizer
            vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            # Load label encoder
            encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            
            # Load response data
            response_path = os.path.join(model_dir, 'response_data.pkl')
            with open(response_path, 'rb') as f:
                self.response_data = pickle.load(f)
            
            # Load metadata
            metadata_path = os.path.join(model_dir, 'model_metadata.json')
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
            
            print("Models loaded successfully!")
            print(f"Model version: {self.metadata['model_version']}")
            print(f"Training date: {self.metadata['training_date']}")
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def preprocess_text(self, text):
        """
        Clean and preprocess user input text
        """
        if not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def predict_intent(self, user_input):
        """
        Predict the intent of user input
        """
        try:
            # Preprocess input
            processed_input = self.preprocess_text(user_input)
            
            # Vectorize input
            input_vector = self.vectorizer.transform([processed_input])
            
            # Predict intent
            predictions = self.intent_model.predict(input_vector.toarray())
            predicted_class = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            # Get intent label
            intent = self.label_encoder.inverse_transform([predicted_class])[0]
            
            return intent, confidence
            
        except Exception as e:
            print(f"Error predicting intent: {e}")
            return "unknown", 0.0
    
    def find_best_response(self, user_input, intent=None):
        """
        Find the best response using similarity matching
        """
        try:
            # Preprocess input
            processed_input = self.preprocess_text(user_input)
            
            # Vectorize input
            input_vector = self.vectorizer.transform([processed_input])
            
            # Calculate similarities with all stored questions
            similarities = cosine_similarity(
                input_vector, 
                self.response_data['question_vectors']
            )[0]
            
            # Find best match
            best_match_idx = np.argmax(similarities)
            best_similarity = similarities[best_match_idx]
            
            if best_similarity > self.similarity_threshold:
                return self.response_data['responses'][best_match_idx], best_similarity
            else:
                return None, best_similarity
                
        except Exception as e:
            print(f"Error finding response: {e}")
            return None, 0.0
    
    def get_fallback_response(self, intent):
        """
        Get fallback responses based on intent
        """
        fallback_responses = {
            "greeting": "Hello! Welcome to Ornament Tech. I'm here to help you with all your jewelry needs. How can I assist you today?",
            "booking": "I'd be happy to help you book a consultation! You can schedule an appointment through our website, call us, or use WhatsApp. We offer both in-person and virtual consultations.",
            "product_info": "We specialize in bespoke jewelry creation with over 15 years of experience. We work with precious metals, gemstones, and create custom pieces for engagements, weddings, and special occasions.",
            "pricing": "Our prices vary based on materials and complexity. Engagement rings start from £2,500, wedding bands from £800, necklaces from £1,200, and earrings from £600. We work with all budgets.",
            "materials": "We work with a variety of precious metals including 18k gold (yellow, white, rose), platinum, and sterling silver. Each material has unique properties for different jewelry styles.",
            "gemstones": "We source the finest gemstones including diamonds, sapphires, emeralds, rubies, and many other precious and semi-precious stones. Each is carefully selected for quality and beauty.",
            "process": "Our bespoke process involves 4 steps: Consultation (understanding your vision), Design (creating detailed drawings), Craft (expert handcrafting), and Delivery (final piece presentation).",
            "contact": "You can reach us at info@ornamenttech.com, call us at +44 20 7123 4567, or use WhatsApp. We respond within 24 hours and offer virtual consultations worldwide.",
            "care": "To care for your jewelry: clean gently with warm water and mild soap, store in individual pouches, avoid harsh chemicals. We offer professional cleaning and maintenance services.",
            "thanks": "You're very welcome! Is there anything else I can help you with regarding our jewelry services?",
            "goodbye": "Thank you for visiting Ornament Tech! Have a wonderful day, and don't hesitate to reach out if you need any assistance with your jewelry needs.",
            "unknown": "I'm not sure I understand that question. Could you please rephrase it? I'm here to help with information about our jewelry, bespoke process, materials, pricing, or booking consultations."
        }
        
        return fallback_responses.get(intent, fallback_responses["unknown"])
    
    def generate_response(self, user_input):
        """
        Generate a response for user input
        """
        # Predict intent
        intent, intent_confidence = self.predict_intent(user_input)
        
        # Find best matching response
        response, similarity = self.find_best_response(user_input, intent)
        
        # Decision logic for response selection
        if response and similarity > self.similarity_threshold:
            final_response = response
            response_type = "matched"
        elif intent_confidence > self.confidence_threshold:
            final_response = self.get_fallback_response(intent)
            response_type = "fallback"
        else:
            final_response = self.get_fallback_response("unknown")
            response_type = "unknown"
        
        # Add context for certain intents
        if intent == "booking" and response_type != "matched":
            final_response += "\n\nWould you like me to provide you with our contact information to schedule your consultation?"
        
        return {
            "response": final_response,
            "intent": intent,
            "confidence": float(intent_confidence),
            "similarity": float(similarity),
            "response_type": response_type,
            "timestamp": datetime.now().isoformat()
        }
    
    def chat_session(self):
        """
        Interactive chat session for testing
        """
        print("Jewelry Chatbot Loaded!")
        print("Type 'quit' to exit the chat session.")
        print("-" * 50)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Chatbot: Thank you for chatting! Have a wonderful day!")
                break
            
            if not user_input:
                continue
            
            # Generate response
            result = self.generate_response(user_input)
            
            print(f"Chatbot: {result['response']}")
            
            # Debug info (optional)
            if False:  # Set to True for debugging
                print(f"[Intent: {result['intent']}, Confidence: {result['confidence']:.3f}, "
                      f"Similarity: {result['similarity']:.3f}, Type: {result['response_type']}]")

def main():
    """
    Main function to run the chatbot
    """
    chatbot = JewelryChatbot()
    
    if chatbot.load_models():
        # Start interactive chat
        chatbot.chat_session()
    else:
        print("Failed to load models. Please ensure training is completed first.")
        print("Run: python training/train-models.py")

if __name__ == "__main__":
    main()
