import { readFileSync } from 'fs'
import { join } from 'path'

export const maxDuration = 30

const JEWELRY_EXPERTISE = {
  gemstones: {
    diamonds: {
      cuts: ['Round', 'Princess', 'Emerald', 'Asscher', 'Marquise', 'Oval', 'Radiant', 'Pear', 'Heart', 'Cushion'],
      clarity: ['FL', 'IF', 'VVS1', 'VVS2', 'VS1', 'VS2', 'SI1', 'SI2', 'I1', 'I2', 'I3'],
      color: ['D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'],
      characteristics: {
        'Round': 'Maximum brilliance and fire, most popular choice',
        'Princess': 'Modern square cut with brilliant sparkle',
        'Emerald': 'Elegant rectangular step cut, showcases clarity',
        'Oval': 'Elongated brilliance, makes fingers appear longer'
      }
    },
    colored: {
      'Sapphire': 'Exceptional hardness (9/10), available in blue, pink, yellow, white',
      'Ruby': 'The red variety of corundum, symbol of passion and love',
      'Emerald': 'Vivid green beryl, prized for color intensity over clarity',
      'Tanzanite': 'Rare blue-violet stone found only in Tanzania',
      'Aquamarine': 'Light blue beryl, evokes ocean tranquility'
    }
  },
  metals: {
    'Platinum': 'Hypoallergenic, naturally white, extremely durable, premium choice',
    '18k White Gold': 'Durable alloy with rhodium plating, classic appearance',
    '18k Yellow Gold': 'Traditional warm tone, timeless appeal',
    '18k Rose Gold': 'Romantic pink hue from copper content, trending choice',
    '14k Gold': 'More affordable option, good durability for daily wear'
  },
  styles: {
    engagement: [
      'Solitaire: Classic single diamond setting',
      'Halo: Center stone surrounded by smaller diamonds',
      'Three-Stone: Past, present, future symbolism',
      'Vintage: Art deco or Victorian inspired designs',
      'Modern: Clean lines, contemporary aesthetics'
    ],
    wedding: [
      'Classic Band: Simple, timeless design',
      'Diamond Eternity: Diamonds all around the band',
      'Vintage Milgrain: Detailed beaded edges',
      'Modern Geometric: Angular, contemporary shapes'
    ]
  },
  occasions: {
    'Engagement': 'Symbol of commitment, typically 1-3 months salary guide',
    'Wedding': 'Exchange of vows, matching or complementary bands',
    'Anniversary': 'Milestone celebrations, often upgrade or add pieces',
    'Birthday': 'Personal celebration, birthstone jewelry popular',
    'Graduation': 'Achievement recognition, often first fine jewelry piece'
  }
}

const CONVERSATION_CONTEXT = {
  userPreferences: new Map(),
  conversationHistory: new Map(),
  expertiseAreas: ['design consultation', 'gemstone education', 'metal selection', 'sizing guidance', 'care instructions', 'investment advice']
}

const WEBSITE_KNOWLEDGE = `
BRAND: Ornament Tech — Luxury bespoke jewellery atelier specializing in editorial-quality craftsmanship and personalized design experiences.

EXPERTISE AREAS:
- Bespoke Design: From concept to creation, fully personalized jewelry
- Gemstone Curation: Ethically sourced diamonds and precious stones
- Master Craftsmanship: Traditional techniques with modern innovation
- Bridal Collections: Engagement rings and wedding bands
- Fine Jewelry: Necklaces, earrings, bracelets for all occasions

NAVIGATION & SECTIONS:
- Home: Brand overview and featured collections
- Bespoke Process: Complete journey from consultation through delivery
- Collections: Curated designs across all jewelry categories
- Galleries: Professional editorial photography of our work
- Materials: Comprehensive guide to metals, finishes, and durability
- Gemstones: Diamond education, colored stones, and ethical sourcing
- Sizing: Professional ring sizing and measurement guidance
- Appointments: Book personal consultations (in-person or virtual)
- Journal: Design inspiration, craftsmanship stories, jewelry guides
- About: Our story, values, and commitment to excellence
- Contact: Direct communication channels and location information
- FAQ: Comprehensive answers to common questions
- Care: Professional maintenance and cleaning guidance
- Craftsmanship: Detailed look at our techniques and philosophy
- Stores: Atelier locations and private viewing appointments

TONE & EXPERTISE:
- Sophisticated yet approachable, like speaking with a knowledgeable jewelry expert
- Educational focus: Help clients understand quality, value, and options
- Consultative approach: Ask questions to understand needs and preferences
- Always provide specific, actionable guidance with relevant links
`

// Load dataset for product recommendations (supports multiple locations)
function getKaggleDataset() {
  try {
    // Try root-level datasets first, then fallback to ml-chatbot/models where datasets currently live
    const datasetCandidates = [
      {
        jewelry: join(process.cwd(), 'datasets', 'jewelry_dataset.csv'),
        diamonds: join(process.cwd(), 'datasets', 'diamonds_dataset.csv')
      },
      {
        jewelry: join(process.cwd(), 'ml-chatbot', 'models', 'jewelry_dataset.csv'),
        diamonds: join(process.cwd(), 'ml-chatbot', 'models', 'diamonds_dataset.csv')
      }
    ]

    // Resolve the first existing pair
    let jewelryPath = ''
    let diamondsPath = ''
    for (const candidate of datasetCandidates) {
      const jExists = require('fs').existsSync(candidate.jewelry)
      const dExists = require('fs').existsSync(candidate.diamonds)
      if (jExists || dExists) {
        jewelryPath = jExists ? candidate.jewelry : jewelryPath
        diamondsPath = dExists ? candidate.diamonds : diamondsPath
        break
      }
    }
    
    let products: any[] = []
    
    // Load jewelry dataset
    if (jewelryPath && require('fs').existsSync(jewelryPath)) {
      const csvData = readFileSync(jewelryPath, 'utf-8')
      const lines = csvData.split('\n')
      const headers = lines[0].split(',')
      
      const jewelry = lines.slice(1, -1).map((line, index) => {
        const values = line.split(',')
        if (values.length === headers.length) {
          return {
            id: `jewelry_${index + 1}`,
            name: `${values[1]?.replace(/"/g, '')} ${values[0]?.replace(/"/g, '')}`,
            category: values[0]?.replace(/"/g, ''),
            type: values[1]?.replace(/"/g, ''),
            metal: values[2]?.replace(/"/g, ''),
            stone: values[3]?.replace(/"/g, ''),
            price: parseFloat(values[7]) || 0,
            weight: parseFloat(values[4]) || 0,
            source: 'jewelry_kaggle'
          }
        }
        return null
      }).filter(Boolean)
      
      products.push(...jewelry)
    }
    
    // Load diamond dataset (sample for high-value items)
    if (diamondsPath && require('fs').existsSync(diamondsPath)) {
      const csvData = readFileSync(diamondsPath, 'utf-8')
      const lines = csvData.split('\n')
      
      // Take first 50 diamonds as premium items
      const diamonds = lines.slice(1, 51).map((line, index) => {
        const values = line.split(',')
        if (values.length >= 7) {
          return {
            id: `diamond_${index + 1}`,
            name: `${parseFloat(values[0])} Carat ${values[1]} ${values[2]} Diamond`,
            category: 'diamond',
            type: 'ring',
            cut: values[1],
            color: values[2],
            clarity: values[3],
            carat: parseFloat(values[0]),
            price: parseFloat(values[6]) || 0,
            source: 'diamond_kaggle'
          }
        }
        return null
      }).filter(Boolean)
      
      products.push(...diamonds)
    }
    
    return products
  } catch (error) {
    console.error('Error loading Kaggle dataset:', error)
    return []
  }
}

function getLastUserMessage(messages: any[]) {
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].role === "user") return messages[i]
  }
  return null
}

function searchProducts(query: string, products: any[], limit = 4) {
  const searchTerms = query.toLowerCase().split(' ')
  
  const scored = products.map(product => {
    let score = 0
    const searchText = `${product.name} ${product.category} ${product.type} ${product.metal || ''} ${product.stone || ''} ${product.cut || ''} ${product.color || ''}`.toLowerCase()
    
    searchTerms.forEach(term => {
      // Exact matches get higher scores
      if (searchText.includes(term)) {
        score += 2
      }
      // Partial matches
      if (searchText.indexOf(term) !== -1) {
        score += 1
      }
    })
    
    // Boost score for exact phrase matches
    if (searchText.includes(query.toLowerCase())) {
      score += 5
    }
    
    // Boost high-value items slightly
    if (product.price > 5000) {
      score += 0.5
    }
    
    return { ...product, score }
  })
  
  return scored
    .filter(p => p.score > 0)
    .sort((a, b) => {
      // Sort by score first, then by price for tie-breaking
      if (b.score !== a.score) return b.score - a.score
      return b.price - a.price
    })
    .slice(0, limit)
}

function buildAdvancedProductRecommendations(query: string, userContext?: any): string {
  const products = getKaggleDataset()
  
  if (products.length === 0) {
    return "I'd love to help you find the perfect piece! Our collections span engagement rings, wedding bands, necklaces, and statement pieces. Visit /collections to explore our curated designs, or let's schedule a personal consultation at /appointments where I can show you pieces tailored to your style."
  }
  
  const matches = searchProducts(query, products, 4)
  
  if (matches.length === 0) {
    // Provide intelligent alternatives based on query
    const q = query.toLowerCase()
    if (q.includes('engagement') || q.includes('proposal')) {
      return `I don't see exact matches for "${query}" but I'd love to help you find the perfect engagement ring! Our engagement collection features classic solitaires, romantic halos, and vintage-inspired designs. The most popular choices are:\n\n• **Classic Solitaire**: Timeless single diamond setting\n• **Halo Setting**: Center stone surrounded by smaller diamonds for extra sparkle\n• **Three-Stone**: Symbolic past, present, and future design\n\nWould you like to explore specific diamond shapes or metals? Visit /collections for our full engagement selection, or book a consultation at /appointments for personalized guidance.`
    }
    
    return "I'd be happy to help you find the perfect piece! While I don't see exact matches in our current search, our collections feature carefully curated designs across all categories. Visit /collections to explore everything, or book a personal consultation at /appointments where I can understand your preferences and show you pieces that match your vision perfectly."
  }
  
  let response = "Based on our collection, here are some exquisite pieces I think you'll love:\n\n"
  
  matches.forEach((product, index) => {
    if (product.source === 'diamond_kaggle') {
      response += `**${index + 1}. ${product.name}** - $${product.price.toLocaleString()}\n`
      response += `   ✨ ${product.carat} carat ${product.cut} cut diamond\n`
      response += `   💎 ${product.color} color grade, ${product.clarity} clarity\n`
      response += `   🌟 *Perfect for those seeking exceptional brilliance and fire*\n\n`
    } else {
      response += `**${index + 1}. ${product.name}** - $${product.price.toLocaleString()}\n`
      response += `   ⚡ Crafted in ${product.metal || 'premium metal'}\n`
      response += `   💫 Features ${product.stone || 'carefully selected'} stones\n`
      response += `   ⚖️ ${product.weight}g weight for comfortable daily wear\n\n`
    }
  })
  
  // Add contextual advice
  const q = query.toLowerCase()
  if (q.includes('engagement')) {
    response += `💍 **Engagement Ring Guidance**: Consider the 4 Cs (Cut, Color, Clarity, Carat) and choose a setting that reflects her personal style. Most couples invest 1-3 months' salary.\n\n`
  } else if (q.includes('wedding')) {
    response += `💕 **Wedding Band Tips**: Choose metals that complement the engagement ring, and consider comfort for daily wear.\n\n`
  }
  
  response += `📅 **Next Steps**: Explore our complete Collections at /collections, or book a personal consultation at /appointments to see these pieces and discuss customization options.`
  
  return response
}

// --- Mixed-query understanding helpers ---
function parsePriceRange(q: string): { min?: number; max?: number } {
  const text = q.toLowerCase()
  // between X and Y
  let m = text.match(/between\s*\$?(\d+(?:\.\d+)?)\s*(k)?\s*(and|to|-|\u2013|\u2014)\s*\$?(\d+(?:\.\d+)?)\s*(k)?/)
  if (m) {
    const min = parseFloat(m[1]) * (m[2] ? 1000 : 1)
    const max = parseFloat(m[4]) * (m[5] ? 1000 : 1)
    return { min, max }
  }
  // under/below/less than X
  m = text.match(/(under|below|less than)\s*\$?(\d+(?:\.\d+)?)\s*(k)?/)
  if (m) {
    const max = parseFloat(m[2]) * (m[3] ? 1000 : 1)
    return { max }
  }
  // above/over/greater than X
  m = text.match(/(above|over|greater than)\s*\$?(\d+(?:\.\d+)?)\s*(k)?/)
  if (m) {
    const min = parseFloat(m[2]) * (m[3] ? 1000 : 1)
    return { min }
  }
  // around/about X (use +/- 25%)
  m = text.match(/(around|about|approx(?:\.|imately)?)\s*\$?(\d+(?:\.\d+)?)\s*(k)?/)
  if (m) {
    const center = parseFloat(m[2]) * (m[3] ? 1000 : 1)
    return { min: Math.max(0, center * 0.75), max: center * 1.25 }
  }
  // budget of X
  m = text.match(/budget(?: of)?\s*\$?(\d+(?:\.\d+)?)\s*(k)?/)
  if (m) {
    const max = parseFloat(m[1]) * (m[2] ? 1000 : 1)
    return { min: 0, max }
  }
  // plain dollar number
  m = text.match(/\$?(\d+(?:\.\d+)?)\s*(k)?/)
  if (m) {
    const approx = parseFloat(m[1]) * (m[2] ? 1000 : 1)
    return { min: Math.max(0, approx * 0.7), max: approx * 1.3 }
  }
  return {}
}

function extractEntities(q: string) {
  const text = q.toLowerCase()
  const categories = ['ring', 'necklace', 'earring', 'bracelet', 'pendant', 'chain', 'band']
  const materials = ['platinum', '18k white gold', '18k yellow gold', '18k rose gold', '14k gold', 'gold', 'white gold', 'yellow gold', 'rose gold', 'silver']
  const gemstones = ['diamond', 'ruby', 'emerald', 'sapphire', 'tanzanite', 'aquamarine', 'pearl']
  const diamondCuts = ['round', 'princess', 'emerald', 'asscher', 'marquise', 'oval', 'radiant', 'pear', 'heart', 'cushion', 'ideal', 'premium', 'very good', 'good', 'fair']
  const colors = ['d','e','f','g','h','i','j','k']
  const clarities = ['fl','if','vvs1','vvs2','vs1','vs2','si1','si2','i1','i2','i3']

  const found = {
    categories: [] as string[],
    materials: [] as string[],
    gemstones: [] as string[],
    cuts: [] as string[],
    colors: [] as string[],
    clarities: [] as string[],
    compare: /(compare|vs|versus|which is better|which one)/.test(text)
  }

  for (const c of categories) if (text.includes(c)) found.categories.push(c)
  for (const m of materials) if (text.includes(m)) found.materials.push(m)
  for (const g of gemstones) if (text.includes(g)) found.gemstones.push(g)
  for (const c of diamondCuts) if (text.includes(c)) found.cuts.push(c)
  for (const c of colors) if (new RegExp(`\\b${c}\\b`).test(text)) found.colors.push(c)
  for (const c of clarities) if (new RegExp(`\\b${c}\\b`).test(text)) found.clarities.push(c)

  return found
}

function filterProductsAdvanced(query: string) {
  const products = getKaggleDataset()
  const entities = extractEntities(query)
  const budget = parsePriceRange(query)

  let filtered = products.slice()

  if (entities.categories.length) {
    filtered = filtered.filter(p => entities.categories.some(c => (p.category || '').toLowerCase().includes(c)))
  }
  if (entities.materials.length) {
    filtered = filtered.filter(p => entities.materials.some(m => (p.metal || '').toLowerCase().includes(m)))
  }
  if (entities.gemstones.length) {
    filtered = filtered.filter(p => entities.gemstones.some(g => (p.stone || '').toLowerCase().includes(g)))
  }
  if (typeof budget.min === 'number') {
    filtered = filtered.filter(p => typeof p.price === 'number' && p.price >= (budget.min as number))
  }
  if (typeof budget.max === 'number') {
    filtered = filtered.filter(p => typeof p.price === 'number' && p.price <= (budget.max as number))
  }

  return { filtered, entities, budget, all: products }
}

function summarizeSet(title: string, set: any[], limit = 4) {
  if (set.length === 0) return `${title}: none found\n`
  const min = Math.min(...set.map(p => p.price || 0))
  const max = Math.max(...set.map(p => p.price || 0))
  const avg = Math.round(set.reduce((s, p) => s + (p.price || 0), 0) / Math.max(1, set.length))
  let s = `**${title}** (${set.length.toLocaleString()} matches)\n`
  s += `Price range: $${min.toLocaleString()} - $${max.toLocaleString()} (avg $${avg.toLocaleString()})\n\n`
  set.slice(0, limit).forEach((p, i) => {
    if (p.source === 'diamond_kaggle') {
      s += `${i + 1}. ${p.carat}ct ${p.cut} ${p.color}/${p.clarity} - $${p.price.toLocaleString()}\n`
    } else {
      s += `${i + 1}. ${p.name} - $${p.price.toLocaleString()}\n`
    }
  })
  return s + '\n'
}

function buildSmartReply(input: string): string {
  const { filtered, entities, budget, all } = filterProductsAdvanced(input)

  // Comparison path
  if (entities.compare) {
    // Compare first two categories/materials/gemstones present
    const subjects: { label: string; items: any[] }[] = []
    const pushSubj = (label: string, items: any[]) => subjects.length < 2 && subjects.push({ label, items })

    if (entities.categories.length) {
      const firstTwo = entities.categories.slice(0, 2)
      for (const c of firstTwo) {
        pushSubj(
          `${c}s`,
          all.filter(p => (p.category || '').toLowerCase().includes(c))
        )
      }
    } else if (entities.materials.length) {
      const firstTwo = entities.materials.slice(0, 2)
      for (const m of firstTwo) {
        pushSubj(
          m,
          all.filter(p => (p.metal || '').toLowerCase().includes(m))
        )
      }
    } else if (entities.gemstones.length) {
      const firstTwo = entities.gemstones.slice(0, 2)
      for (const g of firstTwo) {
        pushSubj(
          g,
          all.filter(p => (p.stone || '').toLowerCase().includes(g))
        )
      }
    }

    if (subjects.length === 2) {
      const [a, b] = subjects
      const stats = (items: any[]) => {
        const count = items.length
        const min = Math.min(...items.map(p => p.price || Infinity))
        const max = Math.max(...items.map(p => p.price || 0))
        const avg = Math.round(items.reduce((s, p) => s + (p.price || 0), 0) / Math.max(1, count))
        return { count, min, max, avg }
      }
      const sa = stats(a.items)
      const sb = stats(b.items)
      let out = `Comparison: ${a.label} vs ${b.label}\n\n`
      out += `- ${a.label}: ${sa.count.toLocaleString()} items | $${sa.min.toLocaleString()} - $${sa.max.toLocaleString()} (avg $${sa.avg.toLocaleString()})\n`
      out += `- ${b.label}: ${sb.count.toLocaleString()} items | $${sb.min.toLocaleString()} - $${sb.max.toLocaleString()} (avg $${sb.avg.toLocaleString()})\n\n`
      // Quick guidance
      out += `Guidance: Choose based on your style and budget${typeof budget.max === 'number' ? ` (budget up to $${(budget.max as number).toLocaleString()})` : ''}. I can refine further if you share preferred metals or stones.`
      return out
    }
  }

  // If we have filters or budget, present focused results
  if (filtered.length || typeof budget.min === 'number' || typeof budget.max === 'number') {
    let title = 'Curated matches'
    if (entities.categories.length) title += ` for ${entities.categories.join(', ')}${entities.gemstones.length ? ' with ' + entities.gemstones.join(', ') : ''}${entities.materials.length ? ' in ' + entities.materials.join(', ') : ''}`
    const body = summarizeSet(title, filtered.length ? filtered : all)
    const budgetLine = (typeof budget.min === 'number' || typeof budget.max === 'number')
      ? `Budget filter applied: ${typeof budget.min === 'number' ? '$' + (budget.min as number).toLocaleString() : 'min'} - ${typeof budget.max === 'number' ? '$' + (budget.max as number).toLocaleString() : 'max'}\n\n`
      : ''
    return budgetLine + body + `Next: Want me to narrow by metal, stone, size, or style?`
  }

  // Fallback to existing advanced recommendations if nothing parsed
  return buildAdvancedProductRecommendations(input)
}

// Enhanced ML-powered chatbot integration
async function getMLResponse(userInput: string): Promise<string | null> {
  try {
    // Try to call the ML API if it's running. Try both 127.0.0.1 and localhost to avoid name resolution edge cases.
    const endpoints = ['http://127.0.0.1:5000/chat', 'http://localhost:5000/chat']
    for (const url of endpoints) {
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message: userInput }),
          // Increase timeout a bit for heavier models
          signal: AbortSignal.timeout(10000)
        })

        if (response.ok) {
          const data = await response.json()
          console.log('✅ ML Response received from', url, '- Intent:', data.intent) // Debug log
          if (data && data.response) return data.response
        } else {
          console.log('⚠️ ML endpoint', url, 'returned status', response.status)
        }
      } catch (err) {
        console.log('⚠️ ML fetch to', url, 'failed:', (err as Error).message)
      }
    }
  } catch (error) {
    console.log('⚠️ ML API unavailable (outer), using fallback:', (error as Error).message)
  }
  
  return null // Fall back to rule-based system
}

type Engine = 'ml' | 'dataset'

async function buildIntelligentReply(input: string): Promise<{ text: string; engine: Engine }> {
  // Try ML response first
  const mlResponse = await getMLResponse(input)
  
  if (mlResponse) {
    return { text: mlResponse, engine: 'ml' }
  }
  
  // Fall back to smarter dataset-backed routing if ML fails
  const q = input.toLowerCase()
  if (/(compare|vs|versus|which is better|which one)/.test(q)) {
    return { text: buildSmartReply(input), engine: 'dataset' }
  }
  return { text: buildRuleBasedResponse(input), engine: 'dataset' }
}

function buildRuleBasedResponse(input: string): string {
  const q = input.toLowerCase()
  const allProducts = getKaggleDataset()

  // Explain how the chatbot works, ML model, and datasets
  if (/\b(how (doe[s]?|does) (it|this|the (chat|chatbot|bot|assistant)) work|what (is|about) (the )?(ml|ai|model)|machine learning|trained|training|dataset|data set|knowledge base|data source)/i.test(q)) {
    return [
      'Here\'s how I work:',
      '',
      '1) ML-first engine:',
      '- I try a local ML service (on http://localhost:5000/chat) trained to understand jewelry intents and craft natural answers.',
      '- If it\'s healthy, you\'ll see Engine: ML in the chat header.',
      '',
      '2) Dataset-backed fallback:',
      '- When ML isn\'t available, I switch to a smart rules engine grounded in our product datasets.',
      '- I load two CSV datasets: a jewelry catalog and a diamonds dataset, then parse your message for category, metal, gemstone, budget, and comparisons.',
      '- I can handle mixed queries like “compare platinum vs gold bands under $2k” or “oval diamond rings around $7k”.',
      '',
      '3) What I return:',
      '- Curated matches, price ranges, and quick guidance, plus links to sections like /collections and /appointments.',
      '',
      'Notes:',
      '- The ML call has a short timeout; if it fails, I automatically use the dataset engine, so you still get a specific answer.',
      '- The datasets are local CSV files (jewelry and diamonds) that provide categories, metals, stones, weights, and prices.',
    ].join('\n')
  }
  
  // FIRST: Answer direct inventory questions with REAL DATA (expanded patterns)
  if (/(what|which|tell me|list|show).*(type|types|kind|kinds|category|categories|variet(y|ies)|options|jewel)/.test(q) || 
    /(what|which).*(do you (have|sell|carry))/.test(q) ||
    /what.*available/.test(q) ||
    /(catalog|inventory|full (list|range)|entire (collection|range))/.test(q)) {
    
    const categories = new Set<string>()
    const materials = new Set<string>()
    const stones = new Set<string>()
    
    allProducts.forEach(p => {
      if (p.category) categories.add(p.category)
      if (p.metal) materials.add(p.metal)
      if (p.stone && p.stone !== 'None') stones.add(p.stone)
    })
    
    let response = `✨ **Our Complete Jewelry Collection** (${allProducts.length.toLocaleString()} pieces):\n\n`
    
    response += `**Jewelry Categories:**\n`
    Array.from(categories).forEach(cat => {
      const count = allProducts.filter(p => p.category === cat).length
      response += `• ${cat.charAt(0).toUpperCase() + cat.slice(1)}: ${count.toLocaleString()} pieces\n`
    })
    
    response += `\n**Premium Materials:**\n`
    Array.from(materials).slice(0, 10).forEach(mat => {
      const count = allProducts.filter(p => p.metal === mat).length
      response += `• ${mat}: ${count.toLocaleString()} pieces\n`
    })
    
    if (stones.size > 0) {
      response += `\n**Gemstones Available:**\n`
      Array.from(stones).slice(0, 10).forEach(stone => {
        const count = allProducts.filter(p => p.stone === stone).length
        response += `• ${stone}: ${count.toLocaleString()} pieces\n`
      })
    }
    
    const priceRange = allProducts.reduce((acc, p) => {
      return {
        min: Math.min(acc.min, p.price),
        max: Math.max(acc.max, p.price),
        avg: acc.avg + p.price
      }
    }, { min: Infinity, max: 0, avg: 0 })
    
    priceRange.avg = priceRange.avg / allProducts.length
    
    response += `\n**Price Range:** $${priceRange.min.toLocaleString()} - $${priceRange.max.toLocaleString()}`
    response += `\n**Average Price:** $${Math.round(priceRange.avg).toLocaleString()}\n\n`
    response += `Browse all at /collections or book a consultation at /appointments!`
    
    return response
  }
  
  // Enhanced greetings with jewelry expertise offer
  if (/(^|\b)(hi|hello|hey|good (morning|afternoon|evening))\b/.test(q)) {
    return "Hello! I'm your personal jewelry consultant at Ornament Tech. I specialize in helping you find the perfect piece, whether it's an engagement ring, anniversary gift, or something special just for you. I can guide you through our collections, explain gemstone quality, discuss metal options, or help you start a bespoke design. What brings you here today?"
  }
  
  // Gratitude responses with additional offer
  if (/\b(thank(s| you)|thanks)\b/.test(q)) {
    return "You're very welcome! I'm here whenever you need guidance on jewelry selection, gemstone education, or design consultation. Feel free to ask me anything about our collections or book a personal appointment at /appointments."
  }

  // Enhanced product searches with better context (relaxed matching)
  if (
    /(ring|necklace|earring|bracelet|pendant|chain|diamond|ruby|emerald|sapphire|gemstone|gold|silver|platinum)/i.test(q) ||
    /(looking for|want|need|show me|find|search|recommend|help me|interested in|browse)/i.test(q)
  ) {
    return buildAdvancedProductRecommendations(input)
  }

  // Engagement ring specific guidance
  if (/(engagement|proposal|propose|marry|marriage)/i.test(q)) {
    return `💍 **Engagement Ring Consultation**\n\nChoosing an engagement ring is one of life's most meaningful purchases. Here's how I can help:\n\n**Understanding the 4 Cs:**\n• **Cut**: Determines brilliance and sparkle\n• **Color**: D-F colorless, G-J near colorless\n• **Clarity**: VS1-VS2 excellent value, SI1-SI2 good value\n• **Carat**: Size preference and budget consideration\n\n**Popular Styles:**\n• Classic Solitaire: Timeless and elegant\n• Halo Setting: Maximum sparkle and visual size\n• Three-Stone: Symbolic and sophisticated\n• Vintage: Unique character and artistry\n\n**Budget Guidance**: Traditionally 1-3 months' salary, but choose what feels right for you.\n\nExplore our engagement collection at /collections or book a personal consultation at /appointments where I can show you diamonds and discuss customization options.`
  }

  // Wedding band guidance
  if (/(wedding|band|bands|marry|marriage)/i.test(q) && !/(engagement)/i.test(q)) {
    return `💕 **Wedding Band Consultation**\n\nWedding bands symbolize eternal love and should complement your engagement ring beautifully:\n\n**Metal Matching:**\n• Same metal as engagement ring for seamless look\n• Mixed metals for contemporary contrast\n• Consider lifestyle and skin sensitivity\n\n**Popular Styles:**\n• Classic comfort fit band\n• Diamond eternity or partial eternity\n• Vintage milgrain or engraved details\n• Modern geometric or organic shapes\n\n**Considerations:**\n• Width that complements engagement ring\n• Comfort for daily wear\n• Matching sets vs. individual pieces\n\nVisit /collections for our wedding band selection or book an appointment at /appointments to see how different bands pair with your engagement ring.`
  }

  // Gemstone education
  if (/(gemstone|gem|diamond|ruby|emerald|sapphire|tanzanite|aquamarine)/i.test(q) && 
      /(learn|tell me|explain|difference|quality|grade|choose)/i.test(q)) {
    const stone = q.match(/(diamond|ruby|emerald|sapphire|tanzanite|aquamarine)/i)?.[0]?.toLowerCase()
    
    if (stone === 'diamond') {
      return `💎 **Diamond Education**\n\nDiamonds are graded on the 4 Cs:\n\n**Cut Quality** (Most Important):\n• Excellent: Maximum brilliance\n• Very Good: Great value and beauty\n• Good: Budget-friendly option\n\n**Color Grades**:\n• D-F: Colorless (premium)\n• G-H: Near colorless (excellent value)\n• I-J: Slight tint (good value)\n\n**Clarity Grades**:\n• FL-IF: Flawless (rare and expensive)\n• VVS1-VVS2: Very very slightly included\n• VS1-VS2: Very slightly included (sweet spot)\n• SI1-SI2: Slightly included (good value)\n\n**Carat Weight**: Size preference within budget\n\nLearn more at /gemstones or book a consultation at /appointments to see diamonds in person and understand quality differences.`
    } else if (stone) {
      const capitalizedStone = stone.charAt(0).toUpperCase() + stone.slice(1) as keyof typeof JEWELRY_EXPERTISE.gemstones.colored
      const info = JEWELRY_EXPERTISE.gemstones.colored[capitalizedStone]
      if (info) {
        return `💎 **${capitalizedStone} Education**\n\n${info}\n\nColored gemstones are prized for their beauty, rarity, and symbolic meaning. Quality factors include color saturation, clarity, cut, and origin.\n\nExplore our gemstone collection at /gemstones or book a consultation at /appointments to see these magnificent stones in person.`
      }
    }
    
    return `💎 **Gemstone Guidance**\n\nWe specialize in both diamonds and colored gemstones:\n\n**Diamonds**: Classic choice, maximum brilliance\n**Sapphires**: Available in many colors, excellent durability\n**Emeralds**: Vivid green, symbol of renewal\n**Rubies**: Passionate red, symbol of love\n\nEach gemstone has unique characteristics and grading criteria. Visit /gemstones for detailed information or book a consultation at /appointments for hands-on education.`
  }

  // Top intents → enhanced responses with more guidance
  if (q.includes("bespoke") || q.includes("custom") || q.includes("design")) {
    return `✨ **Bespoke Design Process**\n\nCreating a custom piece is our specialty! Here's your journey:\n\n**1. Consultation** (Free)\n• Discuss your vision and inspiration\n• Review design options and materials\n• Understand timeline and investment\n\n**2. Design Development**\n• Sketch concepts and CAD renderings\n• Select gemstones and metals\n• Refine every detail together\n\n**3. Master Craftsmanship**\n• Hand-crafted by our artisans\n• Quality checkpoints throughout\n• Photo updates during creation\n\n**4. Delivery & Aftercare**\n• Personal presentation\n• Lifetime care guidance\n• Resize and maintenance services\n\nExplore the complete process at /bespoke-process or start with a consultation at /appointments.`
  }

  if (q.includes("collection") || q.includes("browse") || q.includes("show me")) {
    return `🎨 **Our Collections**\n\nDiscover carefully curated designs across all categories:\n\n**Bridal Collection**:\n• Engagement rings: Solitaires, halos, vintage styles\n• Wedding bands: Classic, diamond, unique designs\n\n**Fine Jewelry**:\n• Necklaces: Delicate chains to statement pieces\n• Earrings: Studs, drops, chandelier styles\n• Bracelets: Tennis, bangles, charm styles\n\n**Signature Pieces**:\n• Limited edition designs\n• Artist collaborations\n• Heirloom-quality statement jewelry\n\nBrowse collections at /collections or see high-resolution imagery at /galleries. Book an appointment at /appointments to view pieces in person.`
  }

  if (q.includes("price") || q.includes("cost") || q.includes("budget") || q.includes("investment")) {
    return `💰 **Investment Guidance**\n\nFine jewelry is a significant investment. Here's helpful guidance:\n\n**Engagement Rings**:\n• $2,000-$5,000: Beautiful options with excellent value\n• $5,000-$10,000: Premium quality and size\n• $10,000+: Exceptional stones and settings\n\n**Wedding Bands**:\n• $800-$2,000: Classic styles in quality metals\n• $2,000+: Diamond or intricate designs\n\n**Fine Jewelry**:\n• Varies by piece, materials, and gemstones\n• Custom designs quoted individually\n\n**Value Factors**:\n• Quality of materials and craftsmanship\n• Timeless design vs. trendy styles\n• Certification and warranties\n\nFor specific pricing, visit /faq or book a consultation at /appointments for personalized guidance within your budget.`
  }

  // Continue with other enhanced responses...
  if (q.includes("material") || q.includes("metal") || q.includes("platinum") || q.includes("gold")) {
    return `⚡ **Metal Selection Guide**\n\nChoosing the right metal affects both beauty and durability:\n\n**Platinum** (Premium Choice):\n• Naturally white, won't tarnish\n• Hypoallergenic and pure\n• Most durable for daily wear\n• Investment-grade quality\n\n**18k Gold Options**:\n• White Gold: Classic, rhodium-plated finish\n• Yellow Gold: Traditional, warm appearance\n• Rose Gold: Romantic, trending choice\n• All excellent durability\n\n**14k Gold**:\n• More affordable option\n• Good durability for active lifestyles\n• Available in all color options\n\n**Selection Tips**:\n• Consider skin tone and personal style\n• Match existing jewelry if desired\n• Think about maintenance preferences\n\nLearn more at /materials or discuss options during a consultation at /appointments.`
  }

  if (q.includes("size") || q.includes("sizing") || q.includes("measure") || q.includes("fit")) {
    return `📏 **Ring Sizing Guidance**\n\nProper sizing ensures comfort and security:\n\n**Professional Sizing** (Recommended):\n• Visit our studio for precise measurement\n• Consider finger changes throughout day\n• Account for knuckle size vs. finger base\n\n**At-Home Methods**:\n• Use our sizing guide at /sizing\n• String or paper wrap method\n• Existing ring comparison\n\n**Important Considerations**:\n• Fingers change size with temperature\n• Wider bands feel tighter\n• Different fingers may vary in size\n• Pregnancy and weight changes affect sizing\n\n**Our Promise**:\n• Free sizing within 30 days\n• Lifetime resize services available\n• Emergency sizing appointments\n\nVisit /sizing for detailed guides or book an appointment at /appointments for professional fitting.`
  }

  if (q.includes("book") || q.includes("appointment") || q.includes("consultation") || q.includes("visit")) {
    return `📅 **Book Your Personal Consultation**\n\nExperience personalized service with our jewelry experts:\n\n**Consultation Options**:\n• **In-Person**: Full sensory experience with our collection\n• **Virtual**: Convenient video consultation\n• **Phone**: Quick guidance and questions\n\n**What to Expect**:\n• 60-90 minute dedicated time\n• Expert guidance on all aspects\n• See diamonds and gemstones up close\n• Discuss customization options\n• No pressure, educational focus\n\n**Popular Consultation Topics**:\n• Engagement ring selection\n• Custom design development\n• Gemstone education\n• Investment and value guidance\n• Care and maintenance tips\n\n**Preparation Tips**:\n• Bring inspiration photos\n• Consider your lifestyle needs\n• Think about budget parameters\n• List any questions\n\nBook your consultation at /appointments - it's complimentary and there's no obligation.`
  }

  // Default enhanced response
  const products = getKaggleDataset()
  const productCount = products.length
  
  return `Welcome to Ornament Tech! I'm your personal jewelry consultant, here to help you navigate our world of fine jewelry and bespoke design.\n\n✨ **I can help you with**:\n• Finding the perfect engagement ring or wedding bands\n• Understanding gemstone quality and value\n• Exploring our ${productCount.toLocaleString()} piece collection\n• Custom design consultation\n• Metal and material selection\n• Sizing and care guidance\n\n🎯 **Popular starting points**:\n• Browse Collections: /collections\n• Learn about Gemstones: /gemstones  \n• Understand our Bespoke Process: /bespoke-process\n• Book a Personal Consultation: /appointments\n\nWhat aspect of jewelry would you like to explore today?`
}

// Minimal SSE response compatible with AI SDK consumers
function fallbackSseResponse(text: string, engine?: 'ml' | 'dataset'): Response {
  const id = `fallback-${Date.now()}`
  const messageEvent =
    `event: message\n` +
    `data: ${JSON.stringify({ id, role: "assistant", content: [{ type: "text", text }], createdAt: new Date().toISOString(), engine })}\n\n`
  const finishEvent = `event: finish\n` + `data: ${JSON.stringify({ id, finishReason: "stop" })}\n\n`

  const body = new ReadableStream({
    start(controller) {
      controller.enqueue(new TextEncoder().encode(messageEvent))
      controller.enqueue(new TextEncoder().encode(finishEvent))
      controller.close()
    },
  })

  return new Response(body, {
    headers: {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
    status: 200,
  })
}

export async function POST(req: Request) {
  const body = await req.json()
  const { messages, message } = body
  
  // Handle different input formats
  let userInput = ''
  
  if (message) {
    // Direct message format
    userInput = typeof message === 'string' ? message : ''
  } else if (messages && Array.isArray(messages)) {
    // AI SDK messages format
    const lastUserMessage = getLastUserMessage(messages)
    userInput = typeof lastUserMessage?.content === 'string' 
      ? lastUserMessage.content 
      : Array.isArray(lastUserMessage?.content)
        ? lastUserMessage.content.map((c: any) => c.type === 'text' ? c.text : c.text || c).join(' ')
        : messages[messages.length - 1]?.content || ''
  }

  // Use ML-powered intelligent responses
  const reply = await buildIntelligentReply(userInput)
  return fallbackSseResponse(reply.text, reply.engine)
}
