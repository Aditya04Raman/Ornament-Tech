import json
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import pickle
import os
import re
from datetime import datetime

class JewelryBotTrainer:
    def __init__(self):
        """
        Initialize the ML trainer for jewelry chatbot
        """
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        self.label_encoder = LabelEncoder()
        self.intent_model = None
        self.response_model = None
        self.training_data = None
        self.intents_data = None
        
    def load_data(self):
        """
        Load training data and intent data
        """
        try:
            # Load training data
            training_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'training-data.json')
            with open(training_path, 'r', encoding='utf-8') as f:
                self.training_data = json.load(f)
            
            # Load intent data
            intent_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'intents.json')
            with open(intent_path, 'r', encoding='utf-8') as f:
                self.intents_data = json.load(f)
                
            print(f"Loaded {self.training_data['total_samples']} training samples")
            print(f"Loaded {len(self.intents_data)} intent categories")
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def preprocess_text(self, text):
        """
        Clean and preprocess text data
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
    
    def create_intent_training_data(self):
        """
        Create training data for intent classification
        """
        intent_texts = []
        intent_labels = []
        
        # Create training samples from intent patterns
        for intent, patterns in self.intents_data.items():
            for pattern in patterns:
                intent_texts.append(self.preprocess_text(pattern))
                intent_labels.append(intent)
        
        # Add questions from training data with appropriate intents
        for question, answer in self.training_data['training_pairs']:
            processed_question = self.preprocess_text(question)
            
            # Classify based on keywords
            if any(word in processed_question for word in ['price', 'cost', 'much', 'expensive', 'budget']):
                intent = 'pricing'
            elif any(word in processed_question for word in ['book', 'appointment', 'schedule', 'consultation']):
                intent = 'booking'
            elif any(word in processed_question for word in ['contact', 'phone', 'email', 'address', 'location']):
                intent = 'contact'
            elif any(word in processed_question for word in ['gold', 'platinum', 'silver', 'metal', 'material']):
                intent = 'materials'
            elif any(word in processed_question for word in ['diamond', 'gemstone', 'stone', 'ruby', 'sapphire']):
                intent = 'gemstones'
            elif any(word in processed_question for word in ['process', 'how', 'steps', 'work']):
                intent = 'process'
            elif any(word in processed_question for word in ['care', 'clean', 'maintain', 'repair']):
                intent = 'care'
            else:
                intent = 'product_info'
            
            intent_texts.append(processed_question)
            intent_labels.append(intent)
        
        return intent_texts, intent_labels
    
    def train_intent_classifier(self):
        """
        Train the intent classification model
        """
        print("Training intent classifier...")
        
        # Create training data
        intent_texts, intent_labels = self.create_intent_training_data()
        
        # Vectorize text
        X = self.vectorizer.fit_transform(intent_texts)
        y = self.label_encoder.fit_transform(intent_labels)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Create neural network model
        self.intent_model = tf.keras.Sequential([
            tf.keras.layers.Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.3),
            tf.keras.layers.Dense(len(np.unique(y)), activation='softmax')
        ])
        
        # Compile model
        self.intent_model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Train model
        history = self.intent_model.fit(
            X_train.toarray(), y_train,
            epochs=50,
            batch_size=32,
            validation_data=(X_test.toarray(), y_test),
            verbose=1
        )
        
        # Evaluate
        y_pred = np.argmax(self.intent_model.predict(X_test.toarray()), axis=1)
        accuracy = accuracy_score(y_test, y_pred)
        
        print(f"Intent Classifier Accuracy: {accuracy:.4f}")
        print("Classification Report:")
        print(classification_report(y_test, y_pred, target_names=self.label_encoder.classes_))
        
        return history
    
    def create_response_mapping(self):
        """
        Create a mapping of questions to responses for similarity matching
        """
        questions = []
        responses = []
        
        for question, answer in self.training_data['training_pairs']:
            questions.append(self.preprocess_text(question))
            responses.append(answer)
        
        return questions, responses
    
    def train_response_generator(self):
        """
        Create response generation system using similarity matching
        """
        print("Creating response generation system...")
        
        # Get question-response pairs
        questions, responses = self.create_response_mapping()
        
        # Vectorize questions for similarity matching
        question_vectors = self.vectorizer.transform(questions)
        
        # Store for later use
        self.response_data = {
            'questions': questions,
            'responses': responses,
            'question_vectors': question_vectors
        }
        
        print(f"Response system created with {len(questions)} question-response pairs")
    
    def save_models(self):
        """
        Save trained models and preprocessors
        """
        model_dir = os.path.join(os.path.dirname(__file__), '..', 'models')
        
        # Save intent model
        intent_model_path = os.path.join(model_dir, 'intent_model.h5')
        self.intent_model.save(intent_model_path)
        
        # Save vectorizer
        vectorizer_path = os.path.join(model_dir, 'vectorizer.pkl')
        with open(vectorizer_path, 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        # Save label encoder
        encoder_path = os.path.join(model_dir, 'label_encoder.pkl')
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        
        # Save response data
        response_path = os.path.join(model_dir, 'response_data.pkl')
        with open(response_path, 'wb') as f:
            pickle.dump(self.response_data, f)
        
        # Save model metadata
        metadata = {
            'training_date': datetime.now().isoformat(),
            'model_version': '1.0',
            'training_samples': self.training_data['total_samples'],
            'intent_classes': self.label_encoder.classes_.tolist(),
            'categories': self.training_data['categories']
        }
        
        metadata_path = os.path.join(model_dir, 'model_metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"Models saved to {model_dir}")
    
    def train_full_pipeline(self):
        """
        Train the complete chatbot pipeline
        """
        print("Starting ML training pipeline for Jewelry Chatbot...")
        
        # Load data
        if not self.load_data():
            print("Failed to load data. Please run data generation first.")
            return False
        
        # Train intent classifier
        self.train_intent_classifier()
        
        # Train response generator
        self.train_response_generator()
        
        # Save models
        self.save_models()
        
        print("Training completed successfully!")
        return True

def main():
    """
    Main training function
    """
    trainer = JewelryBotTrainer()
    success = trainer.train_full_pipeline()
    
    if success:
        print("\n=== Training Summary ===")
        print("✓ Intent classifier trained")
        print("✓ Response generator created")
        print("✓ Models saved to models/ directory")
        print("✓ Ready for chatbot integration")
    else:
        print("Training failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
