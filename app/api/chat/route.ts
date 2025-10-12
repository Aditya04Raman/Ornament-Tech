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

function getLastUserMessage(messages: any[]) {
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].role === "user") return messages[i]
  }
  return null
}

function buildFallbackReply(input: string): string {
  const q = input.toLowerCase()
  // Greetings and small talk
  if (/(^|\b)(hi|hello|hey|good (morning|afternoon|evening))\b/.test(q)) {
    return "Hello! I'm the Ornament Tech concierge. I can help with bespoke consultations, collections, gemstones, sizing, and bookings. What would you like to explore?"
  }
  if (/\b(thank(s| you)|thanks)\b/.test(q)) {
    return "You're welcome! If you need anything else, I'm here to help."
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

  // Generic helpful reply with navigation
  return "I can help you explore bespoke consultations, collections, gemstones, sizing, and bookings. Try: /bespoke-process, /collections, /galleries, /materials, /gemstones, /sizing, or book at /appointments."
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

  try {
    // Call the ML chatbot API
    const response = await fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: userInput
      })
    })

    if (response.ok) {
      const mlResponse = await response.json()
      
      // Use the ML model's response
      const reply = mlResponse.response || buildFallbackReply(userInput)
      
      return fallbackSseResponse(reply)
    } else {
      throw new Error(`ML API returned ${response.status}`)
    }
  } catch (error) {
    console.error('ML Chatbot API Error:', error)
    
    // Fallback to rule-based responses if ML API fails
    const reply = buildFallbackReply(userInput)
    return fallbackSseResponse(`${reply}\n\n(Note: Running in fallback mode)`)
  }
}
