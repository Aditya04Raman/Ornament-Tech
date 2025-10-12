from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add the api directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from chatbot import JewelryChatbot
except ImportError:
    print("Warning: Could not import JewelryChatbot. Please ensure all dependencies are installed.")
    JewelryChatbot = None

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Global chatbot instance
chatbot_instance = None

def initialize_chatbot():
    """
    Initialize the chatbot instance
    """
    global chatbot_instance
    
    if JewelryChatbot is None:
        return False
    
    try:
        chatbot_instance = JewelryChatbot()
        return chatbot_instance.load_models()
    except Exception as e:
        print(f"Error initializing chatbot: {e}")
        return False

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    return jsonify({
        "status": "healthy",
        "service": "Jewelry Chatbot API",
        "chatbot_ready": chatbot_instance is not None
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    """
    try:
        # Check if chatbot is initialized
        if chatbot_instance is None:
            return jsonify({
                "error": "Chatbot not initialized",
                "message": "Please ensure the ML models are trained and available"
            }), 500
        
        # Get user input
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                "error": "Invalid request",
                "message": "Please provide a 'message' field in the request body"
            }), 400
        
        user_message = data['message'].strip()
        
        if not user_message:
            return jsonify({
                "error": "Empty message",
                "message": "Please provide a non-empty message"
            }), 400
        
        # Generate response
        result = chatbot_instance.generate_response(user_message)
        
        # Return response
        return jsonify({
            "response": result['response'],
            "intent": result['intent'],
            "confidence": round(result['confidence'], 3),
            "similarity": round(result['similarity'], 3),
            "response_type": result['response_type'],
            "timestamp": result['timestamp']
        })
        
    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/intents', methods=['GET'])
def get_intents():
    """
    Get available intents
    """
    if chatbot_instance is None or chatbot_instance.metadata is None:
        return jsonify({
            "error": "Chatbot not initialized",
            "intents": []
        }), 500
    
    return jsonify({
        "intents": chatbot_instance.metadata.get('intent_classes', []),
        "categories": chatbot_instance.metadata.get('categories', [])
    })

@app.route('/model-info', methods=['GET'])
def get_model_info():
    """
    Get model information
    """
    if chatbot_instance is None or chatbot_instance.metadata is None:
        return jsonify({
            "error": "Chatbot not initialized"
        }), 500
    
    return jsonify(chatbot_instance.metadata)

@app.route('/test', methods=['POST'])
def test_chatbot():
    """
    Test endpoint with predefined questions
    """
    test_questions = [
        "Hello",
        "What is Ornament Tech?",
        "How much do engagement rings cost?",
        "Tell me about the bespoke process",
        "What materials do you use?",
        "How can I book a consultation?",
        "Thank you"
    ]
    
    if chatbot_instance is None:
        return jsonify({
            "error": "Chatbot not initialized",
            "results": []
        }), 500
    
    results = []
    for question in test_questions:
        try:
            result = chatbot_instance.generate_response(question)
            results.append({
                "question": question,
                "response": result['response'],
                "intent": result['intent'],
                "confidence": round(result['confidence'], 3)
            })
        except Exception as e:
            results.append({
                "question": question,
                "error": str(e)
            })
    
    return jsonify({
        "test_results": results,
        "total_questions": len(test_questions)
    })

if __name__ == '__main__':
    print("Starting Jewelry Chatbot API...")
    
    # Initialize chatbot
    if initialize_chatbot():
        print("✓ Chatbot initialized successfully")
    else:
        print("⚠ Chatbot initialization failed - API will run but chat may not work")
        print("Please ensure ML models are trained by running: python training/train-models.py")
    
    # Start Flask app
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
