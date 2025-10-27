# Chatbot Working Questions

## Overview
This document contains verified working questions for the Ornament Tech chatbot. Use these to test functionality and understand the chatbot's capabilities.

---

## Website Section Queries

### Appointments & Consultations
✅ **Working Questions**:
- `appointments`
- `appointents` (typo-tolerant)
- `book appointment`
- `consultation`
- `schedule a visit`
- `I want to book a consultation`

**Expected Response**: Consultation booking information with options (in-person, virtual, phone), what to expect, preparation tips, and link to `/appointments`

---

### Journal & Articles
✅ **Working Questions**:
- `journal`
- `journls` (typo-tolerant)
- `blog`
- `articles`
- `design stories`
- `read your guides`

**Expected Response**: Journal overview with popular article topics, brief descriptions, and link to `/journal`

---

### Collections
✅ **Working Questions**:
- `collections`
- `show me collections`
- `browse jewelry`
- `catalog`
- `what pieces do you have`

**Expected Response**: Collections overview with bridal, fine jewelry, and signature pieces categories, price ranges, and link to `/collections`

---

### Materials & Metals
✅ **Working Questions**:
- `materials`
- `metals`
- `platinum vs gold`
- `what materials do you use`
- `tell me about white gold`

**Expected Response**: Material selection guide covering platinum, 18K gold options (yellow, white, rose), 14K gold, properties, and link to `/materials`

---

### Gemstones
✅ **Working Questions**:
- `gemstones`
- `diamonds`
- `tell me about sapphires`
- `what are the 4 Cs`
- `gemstone education`

**Expected Response**: Gemstone education covering diamonds (4 Cs), colored gemstones (sapphire, ruby, emerald), ethical sourcing, and link to `/gemstones`

---

### Sizing
✅ **Working Questions**:
- `sizing`
- `how do I measure ring size`
- `ring sizing guide`
- `what's my size`

**Expected Response**: Ring sizing guidance with professional and at-home methods, considerations, promises (free sizing within 30 days), and link to `/sizing`

---

### Care & Maintenance
✅ **Working Questions**:
- `care`
- `how do I clean my jewelry`
- `jewelry maintenance`
- `repair services`

**Expected Response**: Care instructions covering cleaning, storage, professional checks, resizing/repairs, and link to `/care`

---

### Stores & Locations
✅ **Working Questions**:
- `stores`
- `locations`
- `where are you located`
- `studio address`
- `visit your boutique`

**Expected Response**: Studio and boutique addresses (London and Cambridge), phone numbers, and link to `/stores`

---

### FAQ
✅ **Working Questions**:
- `faq`
- `questions`
- `warranty`
- `returns`
- `lead times`

**Expected Response**: FAQ highlights covering lead times, resizing, warranty, returns, and link to `/faq`

---

### About
✅ **Working Questions**:
- `about`
- `who are you`
- `your story`
- `brand values`

**Expected Response**: Brand overview covering bespoke design, master craftsmanship, ethical materials, and link to `/about`

---

### Contact
✅ **Working Questions**:
- `contact`
- `email`
- `phone number`
- `how do I reach you`
- `whatsapp`

**Expected Response**: Contact information (email, phone, WhatsApp), link to contact form, and suggestion to book consultation

---

### Galleries
✅ **Working Questions**:
- `galleries`
- `photos`
- `images`
- `show me your work`

**Expected Response**: Gallery information about editorial photography and link to `/galleries`

---

### Craftsmanship
✅ **Working Questions**:
- `craftsmanship`
- `how do you make jewelry`
- `artisan techniques`
- `handmade process`

**Expected Response**: Craftsmanship overview covering traditional techniques, precision, hand-drawn sketches to CAD, and link to `/craftsmanship`

---

### Bespoke Process
✅ **Working Questions**:
- `bespoke`
- `custom design`
- `bespoke process`
- `how does custom work`

**Expected Response**: 4-step bespoke process (consultation, design, craft, delivery) with timelines, what to expect, and link to `/bespoke-process`

---

## Product Queries

### General Product Search
✅ **Working Questions**:
- `show me rings`
- `engagement rings`
- `necklaces`
- `earrings`
- `diamond jewelry`
- `platinum rings`

**Expected Response**: Product recommendations with actual items from dataset, prices, materials, stones, and links to collections

---

### Budget & Price Filtering
✅ **Working Questions**:
- `rings under $5000`
- `necklaces under £2000`
- `jewelry budget $3000`
- `affordable engagement rings`
- `cheap diamonds under $10000`

**Expected Response**: Filtered product list showing items under specified budget with prices, materials, and details

---

### Product Comparisons
✅ **Working Questions**:
- `compare platinum vs gold`
- `white gold vs rose gold`
- `rings vs necklaces`
- `diamond vs sapphire`

**Expected Response**: Comparison with item counts, price ranges, averages, and guidance on choosing based on budget and style

---

### Specific Product Features
✅ **Working Questions**:
- `platinum diamond rings`
- `rose gold necklaces`
- `sapphire earrings`
- `emerald jewelry`

**Expected Response**: Filtered products matching specified metal and gemstone criteria

---

### Price & Investment Guidance
✅ **Working Questions**:
- `how much do engagement rings cost`
- `price range`
- `budget guidance`
- `investment advice`

**Expected Response**: Investment guidance with price ranges for engagement rings, wedding bands, fine jewelry, and value factors

---

## Jewelry Education

### Diamond Education
✅ **Working Questions**:
- `what are the 4 Cs`
- `diamond quality`
- `how to choose a diamond`
- `diamond grading`

**Expected Response**: Diamond education covering cut, color, clarity, carat with grades and recommendations

---

### Engagement Rings
✅ **Working Questions**:
- `engagement ring guide`
- `proposal ring`
- `how to choose an engagement ring`

**Expected Response**: Engagement ring consultation covering 4 Cs, popular styles, budget guidance, and links

---

### Wedding Bands
✅ **Working Questions**:
- `wedding bands`
- `wedding rings`
- `matching bands`

**Expected Response**: Wedding band consultation covering metal matching, styles, considerations, and links

---

### Metal Selection
✅ **Working Questions**:
- `what metal should I choose`
- `platinum or gold`
- `metal durability`

**Expected Response**: Metal selection guide covering platinum, gold options, durability, and selection tips

---

## Conversational Queries

### Greetings
✅ **Working Questions**:
- `hi`
- `hello`
- `hey`
- `good morning`

**Expected Response**: Personalized greeting introducing the jewelry consultant role and offering assistance

---

### Thank You
✅ **Working Questions**:
- `thank you`
- `thanks`
- `appreciate it`

**Expected Response**: Warm acknowledgment with offer for continued assistance

---

### How It Works
✅ **Working Questions**:
- `how do you work`
- `what is your ML model`
- `how does this chatbot work`

**Expected Response**: Detailed explanation of ML-first engine, dataset-backed fallback, training data, and capabilities

---

### Inventory Questions
✅ **Working Questions**:
- `what types of jewelry do you have`
- `what categories`
- `full catalog`
- `show me everything`

**Expected Response**: Complete collection overview with categories, materials, gemstones, price range, and item counts

---

## Unknown/Fallback Queries

### Single Unknown Word
✅ **Working Questions**:
- `xyz` (any unrecognized single word)
- Random short input

**Expected Response**: Quick navigation menu with all website sections and links

---

## Testing Tips

### For Section Queries:
1. Try single words: `appointments`, `journal`, `collections`
2. Try with typos: `appointents`, `journls`
3. Try variations: `book appointment`, `show me collections`

### For Product Queries:
1. Start broad: `rings`, `necklaces`
2. Add filters: `platinum rings`, `diamond necklaces`
3. Add budget: `rings under $5000`
4. Compare: `platinum vs gold rings`

### For Education:
1. Ask about specific topics: `diamond 4 Cs`, `metal selection`
2. Request guidance: `how to choose engagement ring`
3. Request comparisons: `compare sapphire vs ruby`

---

## Expected Behavior

### All Queries Should:
- ✅ Return a response within 2-3 seconds
- ✅ Include relevant links to website sections
- ✅ Provide specific, helpful information
- ✅ Show engine indicator (ML or Dataset)
- ✅ Match user's intent accurately

### Product Queries Should:
- ✅ Show actual products from datasets
- ✅ Include prices, materials, and details
- ✅ Filter correctly by budget/category/material
- ✅ Provide 4-5 product recommendations

### Section Queries Should:
- ✅ Bypass ML for instant response
- ✅ Provide overview of the section
- ✅ Include clear call-to-action link
- ✅ Match section content accurately

---

## Troubleshooting

### If Section Query Returns Products:
- Check that section keywords are in bypass list
- Verify `isSectionQuery` logic in API route
- Ensure section handlers run before product searches

### If Product Query Shows "No Results":
- Verify datasets are loading (`/ml-status`)
- Check query parsing for typos
- Try broader query first, then add filters

### If Response is Generic:
- Check if ML service is running (`/ml-status`)
- Verify dataset grounding in responses
- Review heuristic overrides in ML service

---

## Quick Test Script

Try these questions in order to verify full functionality:

1. `hi` → Greeting
2. `appointments` → Appointment booking info
3. `collections` → Collections overview
4. `rings under $5000` → Filtered ring products
5. `platinum vs gold` → Comparison with stats
6. `how do you work` → System explanation
7. `what are the 4 Cs` → Diamond education
8. `thank you` → Acknowledgment

All should return relevant, specific responses with links! ✅
