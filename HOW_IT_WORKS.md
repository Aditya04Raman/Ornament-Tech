# How the Website Works: ML Model + Dataset Integration

## Architecture Overview

The Ornament Tech website uses a **hybrid intelligent chatbot** that combines machine learning models with dataset-backed responses to provide accurate, context-aware assistance for jewelry shopping and information.

## System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface                          │
│               (Next.js App - Port 3000)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              Chat Widget (React Component)                  │
│         components/chat-widget.tsx                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            Next.js API Route: /api/chat                     │
│         app/api/chat/route.ts                               │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. ML-First Strategy                               │   │
│  │     • Calls Flask ML Service (localhost:5000)       │   │
│  │     • Timeout: 10 seconds                           │   │
│  │     • Returns if ML available                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                         │                                    │
│                         ▼                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  2. Dataset Fallback Engine                         │   │
│  │     • Loads jewelry + diamond CSVs                  │   │
│  │     • Smart query parsing                           │   │
│  │     • Product filtering & search                    │   │
│  │     • Section routing (appointments, etc.)          │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│         Flask ML Service (Python - Port 5000)               │
│         ml_chatbot_with_models.py                           │
│                                                              │
│  • Intent Classification (Neural Network)                   │
│  • Heuristic Override System                               │
│  • Dataset Integration                                      │
│  • Response Generation                                      │
└─────────────────────────────────────────────────────────────┘
```

## Request Flow

### 1. User Sends Message
```
User types: "show me platinum rings under $5000"
```

### 2. Chat Widget Processes
```typescript
// components/chat-widget.tsx
const response = await fetch('/api/chat', {
  method: 'POST',
  body: JSON.stringify({ messages })
})
```

### 3. API Route Decision Tree

#### Path A: Section Query (Bypasses ML)
```typescript
// Check if query is for website sections
if (isSectionQuery) {
  // Immediate response, no ML call
  return buildRuleBasedResponse(input) // Dataset engine
}
```

**Triggers for**: appointments, journal, collections, materials, gemstones, sizing, care, stores, faq, about, contact, galleries, craftsmanship

#### Path B: Product/General Query (ML-First)
```typescript
// Try ML service first
const mlResponse = await getMLResponse(userInput)

if (mlResponse) {
  return { text: mlResponse, engine: 'ml' }
}

// Fallback to dataset engine if ML unavailable
return { text: buildRuleBasedResponse(input), engine: 'dataset' }
```

### 4A. ML Service Processing (if online)

```python
# ml_chatbot_with_models.py

# Step 1: Preprocess input
cleaned_text = clean_text(user_message)

# Step 2: Vectorize with TF-IDF
vectorized = tfidf_vectorizer.transform([cleaned_text])

# Step 3: Predict intent
intent_probs = intent_model.predict(vectorized)
predicted_intent = label_encoder.inverse_transform([np.argmax(intent_probs)])

# Step 4: Heuristic Override (ensures accuracy)
if _is_search_like(user_message):
    response = handle_search(user_message)
elif _is_pricing_like(user_message):
    response = handle_pricing(user_message)
elif _is_appointment_like(user_message):
    response = handle_appointment(user_message)
# ... more overrides

# Step 5: Return grounded response
return {
    'intent': detected_intent,
    'response': dataset_backed_answer
}
```

### 4B. Dataset Engine Processing (if ML offline)

```typescript
// app/api/chat/route.ts

// Parse query for entities
const entities = extractEntities(query)
// -> categories: ['ring']
// -> materials: ['platinum']
// -> budget: { max: 5000 }

// Load datasets
const products = getKaggleDataset()
// -> 4000 jewelry items + 53940 diamonds

// Filter products
let filtered = products.filter(p => 
  p.category === 'ring' &&
  p.metal.includes('platinum') &&
  p.price <= 5000
)

// Build response with actual products
return formattedProductList(filtered)
```

## Engine Selection Logic

### When Section Queries Bypass ML
```typescript
const sectionKeywords = [
  'appointments', 'journal', 'collections', 'materials',
  'gemstones', 'sizing', 'care', 'stores', 'faq',
  'about', 'contact', 'galleries', 'craftsmanship'
]

// Single-word or section-focused queries skip ML
if (isSingleWordSection || isSectionQuery) {
  return buildRuleBasedResponse(input) // Dataset only
}
```

**Why**: Section queries are deterministic and don't need ML classification. Bypassing ML ensures instant, accurate responses.

### When ML is Used
- Product searches ("engagement rings")
- General questions ("what is the bespoke process?")
- Custom design inquiries
- Care and maintenance questions
- Price predictions
- Conversational queries

### When Dataset Engine is Used
- ML service unavailable (offline/timeout)
- Section navigation queries
- Budget filtering ("under $5000")
- Product comparisons
- Inventory questions

## Response Grounding

### Problem: Generic ML Responses
Without grounding, ML might say:
```
"We have many beautiful rings available. Visit our store!"
```

### Solution: Dataset Integration
With dataset grounding:
```
💎 Platinum Rings Under $5,000

1. Classic Solitaire Ring - $4,200
   ⚡ Platinum
   💫 0.75ct Diamond

2. Halo Engagement Ring - $4,850
   ⚡ Platinum
   💫 1.0ct Diamond, SI1 clarity

Browse more at /collections
```

### Implementation
Both ML and Dataset engines load actual product data:

```python
# ML Service
jewelry_df = pd.read_csv('jewelry_dataset.csv')
diamonds_df = pd.read_csv('diamonds_dataset.csv')

def handle_search(query):
    # Filter real products
    matches = jewelry_df[
        (jewelry_df['category'] == parsed_category) &
        (jewelry_df['price'] <= budget)
    ]
    return format_products(matches)
```

```typescript
// Dataset Engine
function getKaggleDataset() {
  const jewelry = loadCSV('jewelry_dataset.csv')
  const diamonds = loadCSV('diamonds_dataset.csv')
  return [...jewelry, ...diamonds]
}
```

## Intelligence Features

### 1. Typo Tolerance
```typescript
function isLike(text, keywords, maxDistance = 2) {
  // Levenshtein distance matching
  // "appointents" → "appointments" ✓
  // "journls" → "journal" ✓
}
```

### 2. Price Parsing
```typescript
parsePriceRange("rings under $5000")
// → { max: 5000 }

parsePriceRange("between $2k and $5k")
// → { min: 2000, max: 5000 }

parsePriceRange("budget of £3000")
// → { max: 3000 }
```

### 3. Entity Extraction
```typescript
extractEntities("platinum diamond rings")
// → {
//     categories: ['ring'],
//     materials: ['platinum'],
//     gemstones: ['diamond']
//   }
```

### 4. Smart Comparisons
```
User: "compare platinum vs gold wedding bands"

Response:
- Platinum: 150 items | $800 - $3,200 (avg $1,800)
- 18K Gold: 200 items | $600 - $2,800 (avg $1,500)

Guidance: Platinum is more durable...
```

## Health Monitoring

### ML Health Endpoint
```bash
GET http://localhost:5000/health

Response:
{
  "status": "healthy",
  "ml_models_loaded": true,
  "engine": "Neural Network ML",
  "jewelry_items": 4000,
  "diamonds": 53940
}
```

### Frontend Health Check
```typescript
// app/api/ml-health/route.ts
// Proxies ML health with caching and retries
// Returns cached data if ML service is down
```

### Status Page
Visit `/ml-status` to see:
- ML service status
- Models loaded
- Dataset counts
- Engine type
- Diagnostics if offline

## Performance Characteristics

| Metric | ML Engine | Dataset Engine |
|--------|-----------|----------------|
| **Response Time** | 50-200ms | 10-50ms |
| **Cold Start** | 3-5 seconds | Instant |
| **Memory** | ~500MB | ~50MB |
| **Accuracy** | High with overrides | Deterministic |
| **Offline Support** | No | Yes |

## Fallback Behavior

```
┌──────────────┐
│ User Query   │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐     Yes    ┌─────────────────┐
│ Section Query?       ├────────────> Dataset Engine  │
└──────┬───────────────┘             └─────────────────┘
       │ No
       ▼
┌──────────────────────┐     Yes    ┌─────────────────┐
│ ML Service Online?   ├────────────> ML Service      │
└──────┬───────────────┘             └─────────────────┘
       │ No
       ▼
┌──────────────────────┐
│ Dataset Engine       │
│ (Smart Fallback)     │
└──────────────────────┘
```

## Key Design Principles

1. **ML-First, Dataset-Grounded**: Use ML intelligence when available, but always ground responses in real product data
2. **Graceful Degradation**: Website remains fully functional if ML service is offline
3. **Fast Section Routing**: Bypass ML for deterministic queries (appointments, journal, etc.)
4. **Hybrid Intelligence**: Combine ML intent classification with rule-based entity extraction
5. **User Experience**: No loading delays - ML timeout ensures dataset fallback within 10s

## Configuration

### ML Service
```python
# ml_chatbot_with_models.py
HOST = '0.0.0.0'
PORT = 5000
ML_TIMEOUT = 10  # seconds
```

### Next.js API
```typescript
// app/api/chat/route.ts
const ML_ENDPOINTS = [
  'http://127.0.0.1:5000/chat',
  'http://localhost:5000/chat'
]
const ML_TIMEOUT = 10000  // 10 seconds
```

### Dataset Paths
```typescript
const DATASET_PATHS = [
  'datasets/jewelry_dataset.csv',
  'datasets/diamonds_dataset.csv',
  'ml-chatbot/models/jewelry_dataset.csv',  // fallback
  'ml-chatbot/models/diamonds_dataset.csv'
]
```

## Development Workflow

1. **Start ML Service** (optional):
   ```bash
   .\.venv\Scripts\Activate.ps1
   python ml_chatbot_with_models.py
   ```

2. **Start Next.js Dev Server**:
   ```bash
   npm run dev
   ```

3. **Test Chatbot**:
   - Navigate to `http://localhost:3000`
   - Open chat widget
   - Try queries from both engines

4. **Monitor Status**:
   - Visit `/ml-status` for ML health
   - Check browser console for engine logs
   - Review terminal output for API calls

## Troubleshooting

### Chatbot Shows Product Results for Section Queries
- Check `buildIntelligentReply` section keyword list
- Verify `isSectionQuery` logic in `/api/chat/route.ts`
- Ensure section handlers run before product searches

### ML Always Offline
- Start Flask service: `python ml_chatbot_with_models.py`
- Check port 5000 availability
- Verify `/health` endpoint responds
- Review Python dependencies

### Wrong Responses
- ML: Check heuristic overrides in `ml_chatbot_with_models.py`
- Dataset: Review entity extraction and filtering logic
- Both: Verify datasets are loading correctly

### Performance Issues
- Enable ML service caching
- Optimize dataset loading (lazy load)
- Review query parsing complexity
- Check for memory leaks in long-running sessions

## Summary

The Ornament Tech chatbot achieves high accuracy through:
- **Dual-engine architecture**: ML for intelligence, dataset for reliability
- **Smart fallbacks**: Always functional, even offline
- **Dataset grounding**: Real product data in every response
- **Hybrid intelligence**: ML classification + rule-based extraction
- **User-first design**: Fast, accurate, helpful responses
