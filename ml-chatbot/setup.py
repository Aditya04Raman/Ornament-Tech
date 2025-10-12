import os
import sys
import subprocess
import json

def run_command(command, description, working_dir=None):
    """
    Run a command and handle errors
    """
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=working_dir,
            capture_output=True, 
            text=True
        )
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            if result.stdout:
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr:
                print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def check_python():
    """
    Check if Python is available
    """
    try:
        result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Python found: {version}")
            return True
        else:
            print("❌ Python not found")
            return False
    except Exception as e:
        print(f"❌ Error checking Python: {e}")
        return False

def install_requirements():
    """
    Install Python requirements
    """
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    requirements_path = os.path.join(ml_dir, "requirements.txt")
    
    if not os.path.exists(requirements_path):
        print("❌ requirements.txt not found")
        return False
    
    # Install requirements
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies",
        working_dir=ml_dir
    )

def generate_data():
    """
    Generate training data
    """
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    utils_dir = os.path.join(ml_dir, "utils")
    
    # First create basic training data manually since we can't run the scraper yet
    data_dir = os.path.join(ml_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    
    # Create basic training data
    basic_training_data = {
        "training_pairs": [
            ("Hello", "Hello! Welcome to Ornament Tech. I'm here to help you with all your jewelry needs. How can I assist you today?"),
            ("What is Ornament Tech?", "Ornament Tech is a luxury jewelry boutique specializing in bespoke jewelry creation with over 15 years of experience."),
            ("How much do engagement rings cost?", "Our engagement rings start from £2,500. Prices vary based on materials, gemstones, and complexity of design."),
            ("Tell me about the bespoke process", "Our bespoke process involves 4 steps: Consultation, Design, Craft, and Delivery. We work closely with you to create your perfect piece."),
            ("What materials do you use?", "We work with 18k gold (yellow, white, rose), platinum, and sterling silver. We also source the finest gemstones including diamonds, sapphires, emeralds, and rubies."),
            ("How can I book a consultation?", "You can book a consultation through our website, call us, or use WhatsApp. We offer both in-person and virtual consultations."),
            ("Do you offer repairs?", "Yes, we offer comprehensive repair services, resizing, cleaning, and maintenance with a lifetime guarantee on our craftsmanship."),
            ("Thank you", "You're very welcome! Is there anything else I can help you with regarding our jewelry services?"),
        ],
        "total_samples": 8,
        "categories": ["brand", "pricing", "process", "materials", "services", "contact"]
    }
    
    training_data_path = os.path.join(data_dir, "training-data.json")
    with open(training_data_path, 'w', encoding='utf-8') as f:
        json.dump(basic_training_data, f, indent=2, ensure_ascii=False)
    
    # Create basic intent data
    basic_intents = {
        "greeting": ["hello", "hi", "hey", "good morning", "good afternoon"],
        "booking": ["book appointment", "schedule consultation", "make appointment"],
        "product_info": ["tell me about", "what is", "describe", "explain"],
        "pricing": ["how much", "what's the price", "cost", "pricing", "budget"],
        "materials": ["gold", "platinum", "silver", "metal", "material"],
        "gemstones": ["diamond", "sapphire", "emerald", "ruby", "gemstone"],
        "process": ["how does it work", "process", "steps", "procedure"],
        "contact": ["contact", "phone", "email", "address", "location"],
        "care": ["care", "maintenance", "clean", "repair", "resize"],
        "thanks": ["thank you", "thanks", "appreciate"],
        "goodbye": ["goodbye", "bye", "see you", "farewell"]
    }
    
    intents_path = os.path.join(data_dir, "intents.json")
    with open(intents_path, 'w', encoding='utf-8') as f:
        json.dump(basic_intents, f, indent=2, ensure_ascii=False)
    
    print("✅ Basic training data generated")
    return True

def train_models():
    """
    Train ML models
    """
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    training_dir = os.path.join(ml_dir, "training")
    
    return run_command(
        f"{sys.executable} train-models.py",
        "Training ML models",
        working_dir=training_dir
    )

def test_api():
    """
    Test the API
    """
    ml_dir = os.path.dirname(os.path.abspath(__file__))
    api_dir = os.path.join(ml_dir, "api")
    
    print("\n🔄 Testing API (this will start the server - press Ctrl+C to stop)")
    print("The API will be available at http://localhost:5000")
    print("Test endpoints:")
    print("  - GET  /health")
    print("  - POST /chat (with JSON: {'message': 'your question'})")
    print("  - POST /test")
    
    return run_command(
        f"{sys.executable} app.py",
        "Starting API server",
        working_dir=api_dir
    )

def main():
    """
    Main setup function
    """
    print("🚀 Setting up ML Chatbot for Ornament Tech")
    print("=" * 50)
    
    # Check Python
    if not check_python():
        print("Please ensure Python is installed and available")
        return
    
    # Install requirements
    print("\n📦 Installing Dependencies...")
    if not install_requirements():
        print("Failed to install requirements. Please check the error messages.")
        return
    
    # Generate data
    print("\n📊 Generating Training Data...")
    if not generate_data():
        print("Failed to generate training data.")
        return
    
    # Train models
    print("\n🤖 Training ML Models...")
    if not train_models():
        print("Failed to train models. Please check the error messages.")
        return
    
    print("\n✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Test the chatbot: python api/chatbot.py")
    print("2. Start the API server: python api/app.py")
    print("3. Test API endpoints at http://localhost:5000")
    
    # Ask if user wants to start the API
    choice = input("\nWould you like to start the API server now? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        test_api()

if __name__ == "__main__":
    main()
