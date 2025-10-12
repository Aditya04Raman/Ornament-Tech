# ML Chatbot for Ornament Tech

This is a machine learning-powered chatbot specifically designed for the Ornament Tech jewelry website. The chatbot is trained on website content and can answer questions about jewelry, bespoke process, materials, pricing, and services.

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
cd ml-chatbot
python setup.py
```

### Option 2: Manual Setup

1. **Install Dependencies**
```bash
cd ml-chatbot
pip install -r requirements.txt
```

2. **Generate Training Data**
```bash
cd utils
python data-generator.py
```

3. **Train Models**
```bash
cd training
python train-models.py
```

4. **Start API Server**
```bash
cd api
python app.py
```

## 📊 Project Structure

```
ml-chatbot/
├── data/                   # Training data and intents
│   ├── training-data.json  # Question-answer pairs
│   └── intents.json       # Intent classifications
├── models/                 # Trained ML models
│   ├── intent_model.h5    # Intent classification model
│   ├── vectorizer.pkl     # Text vectorizer
│   ├── label_encoder.pkl  # Label encoder
│   └── response_data.pkl  # Response matching data
├── training/              # Model training scripts
│   └── train-models.py   # Main training script
├── api/                   # API and inference
│   ├── chatbot.py        # Main chatbot class
│   └── app.py           # Flask API server
├── utils/                 # Utilities
│   ├── website-scraper.py # Content extraction
│   └── data-generator.py  # Training data generation
├── requirements.txt       # Python dependencies
├── setup.py              # Automated setup script
└── README.md             # This file
```

## 🤖 How It Works

### 1. Intent Classification
- Uses TensorFlow neural network to classify user intent
- Supports intents: greeting, booking, product_info, pricing, materials, gemstones, process, contact, care

### 2. Response Generation
- Uses cosine similarity to find best matching responses
- Falls back to intent-based responses when no good match found
- Combines machine learning with rule-based fallbacks

### 3. Training Data
- Extracted from Ornament Tech website content
- Covers brand information, bespoke process, collections, materials, gemstones
- Generated question variations for robust training

## 🌐 API Endpoints

### Base URL: `http://localhost:5000`

#### Health Check
```bash
GET /health
```

#### Chat with Bot
```bash
POST /chat
Content-Type: application/json

{
  "message": "How much do engagement rings cost?"
}
```

Response:
```json
{
  "response": "Our engagement rings start from £2,500. Prices vary based on materials and complexity.",
  "intent": "pricing",
  "confidence": 0.95,
  "similarity": 0.87,
  "response_type": "matched",
  "timestamp": "2024-01-20T10:30:00.000Z"
}
```

#### Test Bot
```bash
POST /test
```

#### Get Available Intents
```bash
GET /intents
```

#### Get Model Information
```bash
GET /model-info
```

## 💡 Usage Examples

### Test the Chatbot Locally
```bash
cd api
python chatbot.py
```

### Example Questions
- "What is Ornament Tech?"
- "How much do engagement rings cost?"
- "Tell me about the bespoke process"
- "What materials do you use?"
- "How can I book a consultation?"
- "Do you offer repairs?"

## 🔧 Integration with Next.js Frontend

To integrate with the main website, you can call the API from your React components:

```javascript
// Example: components/chat-widget.tsx
const sendMessage = async (message) => {
  try {
    const response = await fetch('http://localhost:5000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ message }),
    });
    
    const data = await response.json();
    return data.response;
  } catch (error) {
    console.error('Chat API error:', error);
    return 'Sorry, I am having technical difficulties. Please try again.';
  }
};
```

## 📈 Model Performance

The chatbot uses:
- **Intent Classification**: TensorFlow neural network with 85%+ accuracy
- **Response Matching**: TF-IDF vectorization with cosine similarity
- **Fallback System**: Intent-based responses for coverage

## 🛠️ Development

### Adding New Training Data
1. Edit `utils/data-generator.py`
2. Add new question-answer pairs
3. Retrain models: `python training/train-models.py`

### Improving Models
- Increase training data in `data-generator.py`
- Adjust model architecture in `train-models.py`
- Tune confidence thresholds in `chatbot.py`

### Adding New Intents
1. Update `intents.json` with new intent patterns
2. Add fallback responses in `chatbot.py`
3. Retrain models

## 🔍 Troubleshooting

### Common Issues

**1. Import Errors (numpy, tensorflow, sklearn)**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**2. Models Not Found**
```bash
python training/train-models.py
```

**3. API Connection Issues**
- Ensure Flask server is running on port 5000
- Check CORS settings in `app.py`
- Verify firewall/network settings

**4. Poor Response Quality**
- Add more training data in `data-generator.py`
- Retrain models with more examples
- Adjust similarity thresholds

### Development Mode
Set debug flags in `chatbot.py` to see detailed prediction info:
```python
if True:  # Set to True for debugging
    print(f"[Intent: {result['intent']}, Confidence: {result['confidence']:.3f}]")
```

## 📝 Notes

- This is a **college machine learning project** focusing on custom model training
- Uses **local ML models** (not external APIs like OpenAI)
- Designed specifically for **jewelry industry** knowledge
- **Scalable architecture** for production deployment
- **Educational focus** on ML implementation and training

## 🎯 Future Enhancements

- [ ] Advanced NLP with transformers
- [ ] Voice interaction capabilities
- [ ] Multi-language support
- [ ] Conversation memory/context
- [ ] Integration with booking system
- [ ] Real-time learning from user interactions

---

**Machine Learning Project by:** [Your Name]  
**For:** Ornament Tech Jewelry Website  
**Purpose:** College ML Assignment - Custom Chatbot Training
