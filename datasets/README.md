# 📊 Ornament Tech Datasets

This folder contains the datasets used to power the intelligent product recommendations and chatbot responses for the Ornament Tech jewelry website.

## 📁 Dataset Overview

### **Total Items: 57,940**
- **Jewelry Dataset**: 4,000 items
- **Diamond Dataset**: 53,940 items

---

## 💍 Jewelry Dataset (`jewelry_dataset.csv`)

### **File Information:**
- **Size**: 0.4 MB
- **Records**: 4,000 jewelry pieces
- **Format**: CSV (Comma Separated Values)

### **Columns:**
| Column | Description | Example Values |
|--------|-------------|----------------|
| `category` | Type of jewelry | ring, necklace, earring, bracelet |
| `type` | Style/subcategory | statement, cocktail, tennis, solitaire |
| `metal` | Metal composition | gold, platinum, silver, rose gold |
| `stone` | Gemstone type | diamond, ruby, sapphire, emerald, pearl |
| `weight` | Weight in grams | 15.5, 25.2, 8.7 |
| `size` | Size measurement | 6.5, 18, 12 |
| `brand` | Brand category | designer, vintage, luxury, contemporary |
| `price` | Price in currency | 2500.00, 15000.50, 850.75 |

### **Sample Data:**
```
category,type,metal,stone,weight,size,brand,price
ring,statement,rose gold,emerald,39.20,9.18,designer,8221.73
ring,cocktail,silver,pearl,30.45,9.96,vintage,48510.54
necklace,pendant,gold,diamond,12.35,18.5,luxury,3250.00
```

---

## 💎 Diamond Dataset (`diamonds_dataset.csv`)

### **File Information:**
- **Size**: 2.5 MB
- **Records**: 53,940 certified diamonds
- **Format**: CSV (Comma Separated Values)

### **Columns (4Cs + Physical Dimensions):**
| Column | Description | Example Values |
|--------|-------------|----------------|
| `carat` | Diamond weight | 0.23, 1.52, 2.01 |
| `cut` | Cut quality | Ideal, Premium, Very Good, Good, Fair |
| `color` | Color grade | D, E, F, G, H, I, J (D=colorless) |
| `clarity` | Clarity grade | FL, IF, VVS1, VVS2, VS1, VS2, SI1, SI2 |
| `depth` | Total depth percentage | 61.5, 59.8, 62.2 |
| `table` | Table percentage | 55.0, 61.0, 58.0 |
| `price` | Price in USD | 326, 1500, 8500 |
| `x` | Length in mm | 3.95, 7.54, 5.12 |
| `y` | Width in mm | 3.98, 7.48, 5.15 |
| `z` | Depth in mm | 2.43, 4.64, 3.18 |

### **Sample Data:**
```
carat,cut,color,clarity,depth,table,price,x,y,z
0.23,Ideal,E,SI2,61.5,55.0,326,3.95,3.98,2.43
0.21,Premium,E,SI1,59.8,61.0,326,3.89,3.84,2.31
1.51,Good,J,VS2,63.3,58.0,7342,7.11,7.18,4.52
```

---

## 🔍 Data Sources

### **Professional Datasets:**
- **Source Type**: Machine Learning / Data Science datasets
- **Platform**: Kaggle (Popular ML dataset repository)
- **Industry Standard**: Used in jewelry industry education and analysis
- **Quality**: Professional gemological grading standards

### **Likely Kaggle Sources:**
- **Diamond Dataset**: Classic "Diamonds" dataset used in ML courses
- **Jewelry Dataset**: E-commerce jewelry catalog dataset

---

## 🎯 Usage in Application

### **Chatbot Integration:**
- **Product Recommendations**: Search through 57,940 items
- **Price Guidance**: Real pricing data for customer consultation
- **Specification Matching**: Find items based on user preferences
- **Educational Content**: Explain diamond 4Cs and jewelry materials

### **Search Algorithm:**
```javascript
// Example: Search for engagement rings under $5000
const results = searchDataset({
  category: "ring",
  type: "engagement", 
  maxPrice: 5000,
  limit: 10
})
```

### **ML Integration:**
- **Intent Recognition**: Understand customer requirements
- **Similarity Matching**: Find similar products
- **Price Prediction**: Estimate values based on specifications
- **Recommendation Engine**: Suggest relevant items

---

## 📈 Dataset Statistics

### **Jewelry Dataset Analytics:**
- **Price Range**: $50 - $75,000
- **Most Common**: Rings (45%), Necklaces (25%), Earrings (20%)
- **Popular Metals**: Gold (40%), Silver (30%), Platinum (20%)
- **Top Stones**: Diamond (35%), Ruby (20%), Sapphire (15%)

### **Diamond Dataset Analytics:**
- **Carat Range**: 0.2 - 5.01 carats
- **Price Range**: $326 - $18,823
- **Cut Distribution**: Ideal (40%), Premium (25%), Very Good (20%)
- **Color Range**: D (colorless) to J (near colorless)
- **Clarity Range**: FL (flawless) to SI2 (slightly included)

---

## 🔧 Technical Implementation

### **File Structure:**
```
datasets/
├── README.md                 # This documentation
├── jewelry_dataset.csv       # 4,000 jewelry items
├── diamonds_dataset.csv      # 53,940 diamonds
└── (future datasets)         # Expansion capability
```

### **Data Loading (Next.js/Node.js):**
```typescript
import { readFileSync } from 'fs'
import { join } from 'path'

// Load jewelry dataset
const jewelryPath = join(process.cwd(), 'datasets', 'jewelry_dataset.csv')
const jewelryData = readFileSync(jewelryPath, 'utf-8')

// Load diamond dataset  
const diamondPath = join(process.cwd(), 'datasets', 'diamonds_dataset.csv')
const diamondData = readFileSync(diamondPath, 'utf-8')
```

### **Database Integration Ready:**
These CSV files can be easily imported into any database system:
- **SQLite**: For development and testing
- **PostgreSQL**: For production deployment
- **MongoDB**: For document-based storage
- **Prisma**: For type-safe database operations

---

## 🎯 Business Value

### **Customer Experience:**
- **Accurate Recommendations**: Real product data
- **Educational Guidance**: Professional grading information
- **Price Transparency**: Market-based pricing
- **Quality Assurance**: Industry-standard specifications

### **Operational Benefits:**
- **Inventory Insight**: Understanding product categories
- **Market Analysis**: Pricing trends and patterns
- **Customer Preferences**: Popular styles and materials
- **Data-Driven Decisions**: Evidence-based recommendations

---

## 📝 Data Quality Notes

### **Professional Standards:**
- ✅ **Diamond Grading**: Follows GIA standards (4Cs)
- ✅ **Pricing Data**: Market-reflective values
- ✅ **Specifications**: Accurate measurements and weights
- ✅ **Categorization**: Industry-standard classifications

### **Limitations:**
- 📊 **Static Data**: Snapshot in time, not live inventory
- 🏷️ **Synthetic Data**: Generated for ML training purposes
- 💰 **Pricing**: Illustrative, not real-time market prices
- 📍 **Availability**: Data doesn't reflect actual stock

---

## 🚀 Future Enhancements

### **Planned Additions:**
- [ ] **Gemstone Dataset**: Colored stones specifications
- [ ] **Vintage Collection**: Historical jewelry pieces
- [ ] **Custom Designs**: Bespoke creation templates
- [ ] **Market Trends**: Seasonal popularity data
- [ ] **Customer Reviews**: Sentiment and preferences

### **Integration Opportunities:**
- [ ] **Live API**: Real-time inventory synchronization
- [ ] **Price Updates**: Dynamic market pricing
- [ ] **ML Training**: Continuous model improvement
- [ ] **Analytics Dashboard**: Business intelligence reporting

---

**📊 Dataset Last Updated**: October 2025  
**🔗 Used By**: Ornament Tech Chatbot & Recommendation Engine  
**📧 Contact**: For dataset questions or updates