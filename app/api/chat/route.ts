import { readFileSync } from 'fs'
import { join } from 'path'

export const maxDuration = 30

const WEBSITE_KNOWLEDGE = `
BRAND: Ornament Tech — bespoke jewellery with artistic, editorial presentation.

NAVIGATION & SECTIONS:
- Home: overview and key calls to action.
- Bespoke Process: step-by-step from consultation to design, crafting, and delivery.
- Collections: curated designs by theme (engagement rings, wedding bands, necklaces, earrings).
- Galleries: high-resolution editorial imagery across categories.
- Materials: metals (platinum, gold variants), finishes, durability, care.
- Gemstones: diamonds (4Cs), colored stones (sapphire, emerald, ruby), ethics and sourcing.
- Sizing: ring sizing guidance, international conversions, tips.
- Appointments: book a consultation, in-person or virtual.
- Journal: stories, guides, behind-the-scenes. Each post has its own page.
- About: brand story, values, craftsmanship.
- Contact: email, phone, hours, locations.
- FAQ: common questions (lead times, pricing ranges, resizing, returns).
- Care: cleaning and maintenance best practices.
- Craftsmanship: techniques, design philosophy, atelier details.
- Stores: studio / showroom locations with visiting info.

PRIMARY ACTIONS:
- Explore bespoke process, browse collections and galleries, book consultation, read journal, contact us.

TONE & STYLE:
- Polished, editorial, welcoming, knowledgeable. Keep responses concise, clear, and helpful.
- Always respond in English. Handle greetings and small talk gracefully (hello, hi, good morning, etc.).

GUIDANCE:
- If asked "where is X?", provide the section name and direct link (e.g., /bespoke-process).
- For sales or appointments, suggest "You can book at /appointments".
- For sizes, guide to /sizing and summarize key points.
- For materials/gemstones, summarize essentials and link to /materials or /gemstones.
- If a question is outside site scope, answer briefly and steer back to relevant sections.

SAMPLE LINKS:
- Bespoke Process: /bespoke-process
- Collections: /collections
- Galleries: /galleries
- Materials: /materials
- Gemstones: /gemstones
- Sizing: /sizing
- Appointments: /appointments
- Journal: /journal
- About: /about
- Contact: /contact
- FAQ: /faq
- Care: /care
- Craftsmanship: /craftsmanship
- Stores: /stores
`

// Load Kaggle dataset for product recommendations
function getKaggleDataset() {
  try {
    const jewelryPath = join(process.cwd(), 'ml-chatbot', 'models', 'jewelry_dataset.csv')
    const diamondsPath = join(process.cwd(), 'ml-chatbot', 'models', 'diamonds_dataset.csv')
    
    let products: any[] = []
    
    // Load jewelry dataset
    if (require('fs').existsSync(jewelryPath)) {
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
    if (require('fs').existsSync(diamondsPath)) {
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

function searchProducts(query: string, products: any[], limit = 3) {
  const searchTerms = query.toLowerCase().split(' ')
  
  const scored = products.map(product => {
    let score = 0
    const searchText = `${product.name} ${product.category} ${product.type} ${product.metal || ''} ${product.stone || ''} ${product.cut || ''} ${product.color || ''}`.toLowerCase()
    
    searchTerms.forEach(term => {
      if (searchText.includes(term)) {
        score += 1
      }
    })
    
    // Boost score for exact matches
    if (searchText.includes(query.toLowerCase())) {
      score += 2
    }
    
    return { ...product, score }
  })
  
  return scored
    .filter(p => p.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
}

function buildProductRecommendations(query: string): string {
  const products = getKaggleDataset()
  
  if (products.length === 0) {
    return "I'd be happy to help you explore our collections! Visit /collections to see our curated designs."
  }
  
  const matches = searchProducts(query, products, 3)
  
  if (matches.length === 0) {
    return "I'd be happy to help you find the perfect piece! Visit /collections to explore our full range, or book a consultation at /appointments for personalized recommendations."
  }
  
  let response = "Based on our collection, here are some pieces you might love:\n\n"
  
  matches.forEach((product, index) => {
    if (product.source === 'diamond_kaggle') {
      response += `${index + 1}. **${product.name}** - $${product.price.toLocaleString()}\n`
      response += `   ${product.carat} carat ${product.cut} cut, ${product.color} color, ${product.clarity} clarity\n\n`
    } else {
      response += `${index + 1}. **${product.name}** - $${product.price.toLocaleString()}\n`
      response += `   ${product.metal} construction with ${product.stone} accents (${product.weight}g)\n\n`
    }
  })
  
  response += `You can explore more in our Collections: /collections, or book a consultation to discuss these pieces: /appointments`
  
  return response
}

function buildIntelligentReply(input: string): string {
  const q = input.toLowerCase()
  
  // Greetings and small talk
  if (/(^|\b)(hi|hello|hey|good (morning|afternoon|evening))\b/.test(q)) {
    return "Hello! I'm the Ornament Tech concierge. I can help with bespoke consultations, collections, gemstones, sizing, and bookings. What would you like to explore?"
  }
  if (/\b(thank(s| you)|thanks)\b/.test(q)) {
    return "You're welcome! If you need anything else, I'm here to help."
  }

  // Product searches - check if user is looking for specific items
  if (/(ring|necklace|earring|bracelet|pendant|chain|diamond|ruby|emerald|sapphire|gold|silver|platinum)/i.test(q) && 
      /(looking for|want|need|show me|find|search|recommend)/i.test(q)) {
    return buildProductRecommendations(input)
  }

  // Top intents → links
  if (q.includes("bespoke") || q.includes("custom")) {
    return "Our bespoke process covers consultation, design, crafting, and delivery. Explore it here: /bespoke-process. If you're ready, you can book a consultation at /appointments."
  }
  if (
    q.includes("collection") ||
    q.includes("engagement") ||
    q.includes("wedding") ||
    q.includes("necklace") ||
    q.includes("earring")
  ) {
    return "Browse curated designs in Collections: /collections. For high‑resolution photography, visit our Galleries: /galleries."
  }
  if (q.includes("gallery") || q.includes("galleries") || q.includes("photos") || q.includes("images")) {
    return "Discover our editorial imagery in the Galleries: /galleries."
  }
  if (q.includes("material") || q.includes("metal") || q.includes("platinum") || q.includes("gold")) {
    return "Learn about metals, finishes, durability, and care at /materials. For gemstone guidance, visit /gemstones."
  }
  if (
    q.includes("gem") ||
    q.includes("diamond") ||
    q.includes("sapphire") ||
    q.includes("emerald") ||
    q.includes("ruby")
  ) {
    return "See diamonds (4Cs) and colored stones guidance at /gemstones. We cover ethics, sourcing, and selection tips."
  }
  if (q.includes("size") || q.includes("sizing") || q.includes("measure")) {
    return "For ring sizing, international conversions, and tips, visit /sizing. If in doubt, we recommend a sizing kit or an in‑person fitting."
  }
  if (q.includes("book") || q.includes("appointment") || q.includes("consultation")) {
    return "You can book an in‑person or virtual consultation here: /appointments."
  }
  if (q.includes("journal") || q.includes("blog") || q.includes("guide")) {
    return "Read stories, guides, and behind‑the‑scenes in our Journal: /journal."
  }
  if (q.includes("about") || q.includes("story") || q.includes("values") || q.includes("craft")) {
    return "Learn about our brand, values, and craftsmanship at /about and /craftsmanship."
  }
  if (q.includes("contact") || q.includes("email") || q.includes("phone")) {
    return "You can reach us via /contact. We list email, phone, hours, and locations."
  }
  if (
    q.includes("faq") ||
    q.includes("return") ||
    q.includes("lead time") ||
    q.includes("resizing") ||
    q.includes("price")
  ) {
    return "Common questions are answered at /faq. If you need more detail, I'm happy to help."
  }
  if (q.includes("care") || q.includes("clean") || q.includes("maintenance")) {
    return "For cleaning and maintenance best practices, see /care."
  }
  if (q.includes("store") || q.includes("location") || q.includes("visit") || q.includes("showroom")) {
    return "Find studio / showroom locations and visiting info at /stores."
  }

  // Default response with dataset info
  const products = getKaggleDataset()
  const productCount = products.length
  
  return `I can help you explore bespoke consultations, collections, gemstones, sizing, and bookings. We have ${productCount.toLocaleString()} pieces in our collection! Try: /bespoke-process, /collections, /galleries, /materials, /gemstones, /sizing, or book at /appointments.`
}

// Minimal SSE response compatible with AI SDK consumers
function fallbackSseResponse(text: string): Response {
  const id = `fallback-${Date.now()}`
  const messageEvent =
    `event: message\n` +
    `data: ${JSON.stringify({ id, role: "assistant", content: [{ type: "text", text }], createdAt: new Date().toISOString() })}\n\n`
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

  // Use dataset-powered intelligent responses directly
  const reply = buildIntelligentReply(userInput)
  return fallbackSseResponse(reply)
}
