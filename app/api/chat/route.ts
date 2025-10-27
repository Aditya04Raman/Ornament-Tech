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

// --- Simple fuzzy matching helpers for short/typoed queries ---
function levenshtein(a: string, b: string): number {
  const m = a.length
  const n = b.length
  const dp = Array.from({ length: m + 1 }, () => new Array<number>(n + 1).fill(0))
  for (let i = 0; i <= m; i++) dp[i][0] = i
  for (let j = 0; j <= n; j++) dp[0][j] = j
  for (let i = 1; i <= m; i++) {
    for (let j = 1; j <= n; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1
      dp[i][j] = Math.min(
        dp[i - 1][j] + 1, // deletion
        dp[i][j - 1] + 1, // insertion
        dp[i - 1][j - 1] + cost // substitution
      )
    }
  }
  return dp[m][n]
}

function isLike(text: string, keywords: string[], maxDistance = 2): boolean {
  const q = text.toLowerCase().trim()
  const tokens = q.split(/\s+/)
  for (const kw of keywords) {
    const k = kw.toLowerCase()
    if (q.includes(k)) return true
    if (tokens.includes(k)) return true
    if (tokens.length === 1 && levenshtein(q, k) <= maxDistance) return true
  }
  return false
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
  const q = input.toLowerCase().trim()
  
  // FORCE dataset engine for single-word section queries (even if ML is available)
  // This prevents ML from incorrectly classifying section names as product searches
  const sectionKeywords = [
    'appointments', 'appointment', 'consultation', 'consult', 'book', 'visit', 'appointents',
    'journal', 'journals', 'articles', 'blog', 'guides', 'stories',
    'about', 'brand', 'story', 'values',
    'contact', 'email', 'phone', 'support', 'whatsapp',
    'gallery', 'galleries', 'photos', 'images', 'editorial',
    'care', 'cleaning', 'maintenance', 'service', 'repair', 'resize',
    'stores', 'store', 'location', 'locations', 'studio', 'boutique', 'address',
    'faq', 'questions', 'warranty', 'guarantee', 'returns', 'return',
    'craftsmanship', 'handmade', 'artisan', 'atelier', 'workshop',
    'bespoke', 'bespoke-process', 'process',
    'collections', 'collection', 'catalog',
    'materials', 'material', 'metals',
    'gemstones', 'gemstone', 'diamonds',
    'sizing', 'size', 'measurement'
  ]
  
  const tokens = q.split(/\s+/)
  const isSingleWordSection = tokens.length === 1 && sectionKeywords.some(kw => isLike(q, [kw]))
  const isSectionQuery = sectionKeywords.some(kw => q.includes(kw) || isLike(q, [kw]))
  
  if (isSingleWordSection || isSectionQuery) {
    // Skip ML for section queries - use dataset engine directly
    return { text: buildRuleBasedResponse(input), engine: 'dataset' }
  }
  
  // Try ML response first for other queries
  const mlResponse = await getMLResponse(input)
  
  if (mlResponse) {
    return { text: mlResponse, engine: 'ml' }
  }
  
  // Fall back to smarter dataset-backed routing if ML fails
  const q2 = input.toLowerCase()
  if (/(compare|vs|versus|which is better|which one)/.test(q2)) {
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

  // Journal and editorial content
  if (/(journal|article|blog|guide|story|stories)/i.test(q) || isLike(q, ['journal', 'journals', 'articles', 'blog', 'guides', 'stories'])) {
    return `📝 Journal & Editorial

Our journal explores design inspiration, craftsmanship behind the scenes, gemstone education, and care tips. A few popular reads:

• How to choose the right diamond shape for your style
• Behind the craft: from sketch to finished ring
• Caring for heirloom jewelry: do's and don'ts
• Metal matters: platinum vs. gold explained

Browse all posts at /journal. Tell me what topic you’re interested in and I can summarize or point you to the best article.`
  }

  // About the brand
  if (/(about|your story|who are you|values|brand)/i.test(q) || isLike(q, ['about', 'brand', 'story', 'values'])) {
    return `About Ornament Tech

We’re a bespoke jewelry atelier where traditional craftsmanship meets modern technology. Our focus is:
• Bespoke design: from concept to creation with you
• Master craftsmanship: handmade pieces with precision
• Ethical materials: responsibly sourced gemstones and metals

Learn more at /about or ask me about our bespoke process and services.`
  }

  // Contact and support
  if (/(contact|email|phone|call|whatsapp|support|reach you)/i.test(q) || isLike(q, ['contact', 'email', 'phone', 'support', 'whatsapp'])) {
    return `Contact Us

• Email: hello@ornamenttech.com
• Phone: +44 20 8154 9500
• WhatsApp: https://wa.me/1234567890

You can also reach us via the form at /contact. If you’d like, I can help you book a consultation at /appointments.`
  }

  // Galleries and imagery
  if (/(gallery|galleries|photos|images|editorial)/i.test(q) || isLike(q, ['gallery', 'galleries', 'photos', 'images', 'editorial'])) {
    return `Galleries

Explore editorial-quality photography of our work, from engagement rings to bespoke creations. Visit /galleries for high-resolution imagery, or ask me to guide you to pieces that match your taste.`
  }

  // Care and maintenance
  if (/(care|clean|cleaning|maintenance|polish|service|repair|resize|refinish)/i.test(q) || isLike(q, ['care', 'cleaning', 'maintenance', 'service', 'repair', 'resize'])) {
    return `Jewelry Care & Services

• Cleaning: Warm water, mild soap, and a soft brush; dry with lint-free cloth
• Storage: Separate pouches or compartments to avoid scratches
• Professional check: Annual prong and setting inspection recommended
• Resizing and repairs: Available by appointment

See our full guidance at /care, or book a maintenance appointment at /appointments.`
  }

  // Stores and locations
  if (/(store|stores|location|locations|studio|boutique|address|where are you)/i.test(q) || isLike(q, ['stores', 'store', 'location', 'locations', 'studio', 'boutique', 'address'])) {
    return `Studios & Boutiques

• London Studio: 69 Regent's Park Road, Primrose Hill, London NW1 8UY (020 8154 9500)
• Cambridge Boutique: 6/7 Green Street, Cambridge CB2 3JU (01223 461333)

Plan your visit at /stores or book a consultation at /appointments (in-person or virtual).`
  }

  // FAQ and quick answers
  if (/(faq|questions|lead time|leadtime|warranty|guarantee|returns?)/i.test(q) || isLike(q, ['faq', 'questions', 'warranty', 'guarantee', 'returns', 'return'])) {
    return `FAQ Highlights

• Lead times: Bespoke projects typically take 4–8 weeks depending on complexity
• Ring resizing: Yes, we provide professional sizing and aftercare
• Warranty: Lifetime guarantee covering craftsmanship and materials
• Returns: See policy details at /faq or ask me about a specific case

Read more at /faq, or share your specific question and I’ll answer directly.`
  }

  // Craftsmanship and techniques
  if (/(craftsmanship|technique|handmade|artisan|atelier|workshop)/i.test(q) || isLike(q, ['craftsmanship', 'handmade', 'artisan', 'atelier', 'workshop'])) {
    return `Craftsmanship

Every piece is handmade by our artisans using traditional techniques alongside modern precision. From hand-drawn sketches and CAD to careful stone setting and finishing, we obsess over detail.

Learn more at /craftsmanship or ask about the steps from concept to creation.`
  }

  // Bespoke process
  if (/(bespoke|custom|design|process)/i.test(q) && /(process|journey|how|steps|bespoke)/i.test(q) || isLike(q, ['bespoke', 'bespoke-process', 'process'])) {
    return `✨ Bespoke Design Process

From concept to creation, a guided journey tailored to you:

**1. Consultation** (Week 1)
• Share your vision and story with our designers
• Discuss budget, timeline, and unique inspirations

**2. Design** (Weeks 2-3)
• Hand-drawn sketches and 3D CAD models
• Refine every detail together until perfect

**3. Craft** (Weeks 4-8)
• Master craftspeople bring your design to life
• Traditional techniques with modern precision
• Photo updates during creation

**4. Delivery** (Week 9)
• Rigorous quality checks
• Personal presentation in signature packaging
• Lifetime care and aftercare guidance

Typical timeline: 4-8 weeks depending on complexity.

Explore the complete process at /bespoke-process or start with a free consultation at /appointments.`
  }

  // Collections
  if (/(collections?|browse|catalog|pieces|designs)/i.test(q) && !/(what|types|kinds|categories)/i.test(q) || isLike(q, ['collections', 'collection', 'catalog'])) {
    return `🎨 Our Collections

Discover carefully curated designs across all categories:

**Bridal Collection**
• Engagement rings: 50+ designs from £2,500
• Wedding bands: 40+ designs from £800

**Fine Jewelry**
• Necklaces: 35+ designs from £1,200
• Earrings: 45+ designs from £600
• Bracelets and statement pieces

**Signature Collections**
• Heritage Collection: 30+ timeless designs from £1,800
• Limited editions and artist collaborations

Every piece features ethically sourced materials with full traceability and award-winning craftsmanship.

Browse all at /collections or view high-resolution imagery at /galleries. Book an appointment at /appointments to see pieces in person.`
  }

  // Materials and metals (explicit priority)
  if (/(materials?|metals?|platinum|gold)/i.test(q) && /(guide|about|what|learn|tell me|explain)/i.test(q) || isLike(q, ['materials', 'material', 'metals'])) {
    return `⚡ Material Selection Guide

Choosing the right metal affects both beauty and durability:

**Platinum** (Premium Choice)
• Naturally white, hypoallergenic, extremely durable
• Develops beautiful patina while maintaining strength
• Best for: Engagement rings, daily wear

**18K Gold Options**
• Yellow Gold: Classic warm tone, traditional choice
• White Gold: Modern bright finish, rhodium-plated
• Rose Gold: Romantic blush tone, vintage appeal
• All offer excellent durability

**14K Gold**
• More affordable option with good durability
• Available in all color options

**Selection Tips:**
• Consider skin tone and personal style
• Match existing jewelry if desired
• Think about maintenance preferences and lifestyle

Learn more at /materials or discuss options during a consultation at /appointments.`
  }

  // Gemstones (explicit priority)
  if (/(gemstones?|diamonds?|sapphires?|emeralds?|rubies?)/i.test(q) && /(learn|about|education|guide|what)/i.test(q) || isLike(q, ['gemstones', 'gemstone', 'diamonds'])) {
    return `💎 Gemstone Education

**Diamonds** - Understand the 4Cs
• Cut: Determines brilliance and sparkle (most important)
• Color: D-F colorless, G-J near colorless
• Clarity: VS1-VS2 excellent value, SI1-SI2 good value
• Carat: Size preference within budget

**Colored Gemstones**
• Sapphire: Exceptional hardness, available in many colors
• Ruby: Intense red corundum, symbol of love and passion
• Emerald: Vivid green beryl with natural character
• Tanzanite: Rare blue-violet, found only in Tanzania

**Our Promise:**
• Ethically sourced with full traceability
• Expert guidance on quality and value
• Certification for all diamonds

Learn more at /gemstones or book a consultation at /appointments to see gemstones in person and understand quality differences.`
  }

  // Sizing guide (explicit priority)
  if (/(sizing|size|measure|fit)/i.test(q) && /(ring|guide|how)/i.test(q) || isLike(q, ['sizing', 'size', 'measurement'])) {
    return `📏 Ring Sizing Guide

Proper sizing ensures comfort and security:

**Professional Sizing** (Recommended)
• Visit our studio for precise measurement
• We account for knuckle size and finger changes
• Consider time of day (fingers swell in warmth)

**At-Home Methods**
• Use our printable sizing tools at /sizing
• String or paper wrap method
• Compare with existing rings

**Important Considerations:**
• Wider bands feel tighter than thin bands
• Fingers change with temperature and activity
• Different fingers may vary in size
• Pregnancy and weight changes affect sizing

**Our Promise:**
• Free sizing within 30 days of purchase
• Lifetime resize services available
• Emergency sizing appointments

Visit /sizing for detailed guides, printable tools, and international conversions, or book an appointment at /appointments for professional fitting.`
  }

  // PRIORITY: Appointments/consultation booking (check before product searches)
  if (q.includes("book") || q.includes("appointment") || q.includes("consultation") || q.includes("visit") || isLike(q, ['appointments', 'appointment', 'consultation', 'consult', 'book', 'visit', 'appointents'])) {
    return `📅 **Book Your Personal Consultation**

Experience personalized service with our jewelry experts:

**Consultation Options**:
• **In-Person**: Full sensory experience with our collection
• **Virtual**: Convenient video consultation
• **Phone**: Quick guidance and questions

**What to Expect**:
• 60-90 minute dedicated time
• Expert guidance on all aspects
• See diamonds and gemstones up close
• Discuss customization options
• No pressure, educational focus

**Popular Consultation Topics**:
• Engagement ring selection
• Custom design development
• Gemstone education
• Investment and value guidance
• Care and maintenance tips

**Preparation Tips**:
• Bring inspiration photos
• Consider your lifestyle needs
• Think about budget parameters
• List any questions

Book your consultation at /appointments - it's complimentary and there's no obligation.`
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

  // Price and investment guidance (kept as it's more specific than materials/collections)
  if (q.includes("price") || q.includes("cost") || q.includes("budget") || q.includes("investment")) {
    return `💰 **Investment Guidance**\n\nFine jewelry is a significant investment. Here's helpful guidance:\n\n**Engagement Rings**:\n• $2,000-$5,000: Beautiful options with excellent value\n• $5,000-$10,000: Premium quality and size\n• $10,000+: Exceptional stones and settings\n\n**Wedding Bands**:\n• $800-$2,000: Classic styles in quality metals\n• $2,000+: Diamond or intricate designs\n\n**Fine Jewelry**:\n• Varies by piece, materials, and gemstones\n• Custom designs quoted individually\n\n**Value Factors**:\n• Quality of materials and craftsmanship\n• Timeless design vs. trendy styles\n• Certification and warranties\n\nFor specific pricing, visit /faq or book a consultation at /appointments for personalized guidance within your budget.`
  }

  // Budget-specific jewelry queries (e.g., "rings under $5000", "necklaces under £2000")
  if (/(under|below|less than|budget|affordable|cheap|inexpensive)/i.test(q) && 
      /(ring|necklace|earring|bracelet|jewelry|jewellery|diamond|engagement|wedding)/i.test(q) ||
      /\$\d+|\£\d+|budget of/i.test(q)) {
    const { filtered, entities, budget, all } = filterProductsAdvanced(input)
    
    if (filtered.length > 0) {
      // Show actual filtered products
      let response = `💎 **Budget-Friendly ${entities.categories.length ? entities.categories[0] + 's' : 'Jewelry'}**\n\n`
      
      if (budget.max) {
        response += `Showing pieces under $${budget.max.toLocaleString()}:\n\n`
      }
      
      filtered.slice(0, 4).forEach((product, index) => {
        if (product.source === 'diamond_kaggle') {
          response += `**${index + 1}. ${product.name}** - $${product.price.toLocaleString()}\n`
          response += `   ✨ ${product.carat} carat ${product.cut} cut diamond\n`
          response += `   💎 ${product.color} color, ${product.clarity} clarity\n\n`
        } else {
          response += `**${index + 1}. ${product.name}** - $${product.price.toLocaleString()}\n`
          response += `   ⚡ ${product.metal || 'Premium metal'}\n`
          response += `   💫 ${product.stone || 'Quality stones'}\n\n`
        }
      })
      
      response += `Browse more at /collections or book a consultation at /appointments for personalized recommendations!`
      return response
    } else {
      // Fallback if no matches found
      const maxPrice = budget.max || 5000
      return `💎 **Budget Search Results**\n\nI searched our collection but didn't find exact matches under $${maxPrice.toLocaleString()}. However, we have many beautiful pieces in this range!\n\n**Popular Options**:\n• Engagement rings: $2,000-$5,000\n• Wedding bands: $800-$2,000\n• Fine jewelry: $600-$3,000\n\nTell me more about what you're looking for (style, metal, stone) and I'll find the perfect pieces!\n\nBrowse our collection at /collections or book a consultation at /appointments.`
    }
  }

  // Single-word quick nav if unknown
  const tokenCount = q.trim().split(/\s+/).filter(Boolean).length
  if (tokenCount === 1 && q.length <= 20) {
    return `Quick Navigation:

📅 Appointments: /appointments
📝 Journal: /journal
💍 Collections: /collections
⚡ Materials: /materials
💎 Gemstones: /gemstones
📏 Sizing: /sizing
✨ Bespoke Process: /bespoke-process
🎨 Galleries: /galleries
🔧 Care: /care
🏪 Stores: /stores
🏛️ About: /about
📞 Contact: /contact
❓ FAQ: /faq
🛠️ Craftsmanship: /craftsmanship

Tell me a section name or ask a question (e.g., "engagement rings under $5k", "how does bespoke work?").`
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
