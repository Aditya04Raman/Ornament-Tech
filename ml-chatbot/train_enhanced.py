"""
Script to train the enhanced ML chatbot with real datasets
"""
import sys
import os

# Add the training directory to path
training_dir = os.path.join(os.path.dirname(__file__), 'training')
sys.path.append(training_dir)

# Import the enhanced training module
from enhanced_train_models import EnhancedJewelryBotTrainer

def main():
    print("🚀 Starting Enhanced ML Training with Real Datasets...")
    print("=" * 60)
    
    # Initialize trainer
    trainer = EnhancedJewelryBotTrainer()
    
    # Start training process
    try:
        trainer.train_enhanced_chatbot()
        
        print("\n" + "=" * 60)
        print("✅ TRAINING COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nWhat was trained:")
        print("📊 Real diamond dataset (5000+ samples)")
        print("💎 Comprehensive jewelry dataset (4000+ samples)")  
        print("🤖 Enhanced intent classification model")
        print("💰 Diamond price prediction model")
        print("❓ Dataset-derived Q&A system")
        print("\nModels saved to: ml-chatbot/models/")
        print("\nNext steps:")
        print("1. Update API to use enhanced_chatbot.py")
        print("2. Test the enhanced chatbot")
        print("3. Deploy with real ML capabilities")
        
    except Exception as e:
        print(f"\n❌ Training failed: {e}")
        print("Please check the error and try again.")

if __name__ == "__main__":
    main()