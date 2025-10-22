"use client"

import { useState, useEffect, useRef } from "react"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: Date
  engine?: 'ml' | 'dataset'
}

export default function ChatWidget() {
  const [open, setOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [isTyping, setIsTyping] = useState(false)
  const [engine, setEngine] = useState<'ml' | 'dataset' | 'unknown'>('unknown')
  const [mlStatus, setMlStatus] = useState<'ok' | 'down' | 'checking'>('checking')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Poll ML health every 5 seconds
  useEffect(() => {
    let mounted = true
    async function checkMl() {
      setMlStatus('checking')
      try {
        const r = await fetch('/api/ml-health')
        if (!mounted) return
        if (r.ok) {
          const data = await r.json()
          if (data?.status === 'ok' && data.ml?.ml_models_loaded) {
            setMlStatus('ok')
          } else {
            setMlStatus('down')
          }
        } else {
          setMlStatus('down')
        }
      } catch (e) {
        if (!mounted) return
        setMlStatus('down')
      }
    }
    checkMl()
    const id = setInterval(checkMl, 5000)
    return () => { mounted = false; clearInterval(id) }
  }, [])

  const sendMessage = async (content: string) => {
    if (!content.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: content.trim(),
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInput("")
    setIsLoading(true)
    setIsTyping(true)

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: [...messages, userMessage].map(m => ({
            role: m.role,
            content: [{ type: "text", text: m.content }]
          }))
        }),
      })

      if (response.ok) {
        const reader = response.body?.getReader()
        if (reader) {
          const assistantMessage: Message = {
            id: (Date.now() + 1).toString(),
            role: "assistant",
            content: "",
            timestamp: new Date()
          }
          
          setMessages(prev => [...prev, assistantMessage])
          setIsTyping(false)
          
          while (true) {
            const { done, value } = await reader.read()
            if (done) break
            
            const chunk = new TextDecoder().decode(value)
            const lines = chunk.split('\n')
            
            for (const line of lines) {
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6))
                  if (data.engine && (data.engine === 'ml' || data.engine === 'dataset')) {
                    setEngine(data.engine)
                  }
                  if (data.content && data.content[0]?.text) {
                    setMessages(prev => prev.map(m => 
                      m.id === assistantMessage.id 
                        ? { ...m, content: m.content + data.content[0].text }
                        : m
                    ))
                  }
                } catch (e) {
                  // Ignore parsing errors
                }
              }
            }
          }
        }
      }
    } catch (error) {
      console.error("Chat error:", error)
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: "Hello! I'm the Ornament Tech concierge. I can help with bespoke consultations, collections, gemstones, sizing, and bookings. What would you like to explore?",
        timestamp: new Date()
      }
      setMessages(prev => [...prev, errorMessage])
      setIsTyping(false)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <>
      {/* Enhanced Toggle Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          aria-label="Open Ornament Tech chat"
          onClick={() => setOpen((v) => !v)}
          className={`group relative overflow-hidden rounded-full p-4 shadow-2xl transition-all duration-300 ease-in-out transform hover:scale-110 hover:shadow-3xl ${
            open 
              ? 'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700' 
              : 'bg-gradient-to-r from-primary to-accent hover:from-accent hover:to-primary'
          }`}
        >
          {/* Animated background shimmer */}
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -skew-x-12 transform -translate-x-full group-hover:translate-x-full transition-transform duration-1000 ease-in-out"></div>
          
          {/* Button content */}
          <div className="relative flex items-center gap-3 text-white">
            {open ? (
              <>
                <svg className="w-6 h-6 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span className="font-medium hidden sm:block">Close</span>
              </>
            ) : (
              <>
                <div className="relative">
                  <svg className="w-6 h-6 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                  {/* Online indicator */}
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
                </div>
                <span className="font-medium hidden sm:block">Chat with us</span>
              </>
            )}
          </div>
          
          {/* Notification badge */}
          {!open && messages.length === 0 && (
            <div className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 rounded-full flex items-center justify-center">
              <span className="text-xs text-white font-bold">!</span>
            </div>
          )}
        </button>
      </div>

      {/* Enhanced Chat Panel */}
      {open && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed bottom-24 right-6 z-40 w-[26rem] max-w-[90vw] rounded-2xl overflow-hidden shadow-2xl flex flex-col max-h-[36rem] bg-gradient-to-b from-white to-gray-50 border border-gray-200/50 backdrop-blur-sm"
          style={{
            animation: 'slideUp 0.3s ease-out',
          }}
        >
          {/* Elegant Header */}
          <header className="relative px-6 py-4 bg-gradient-to-r from-primary to-accent text-white">
            <div className="absolute inset-0 bg-black/10"></div>
            <div className="relative">
              <div className="flex items-center gap-3 mb-2">
                <div className="w-10 h-10 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div>
                  <h2 className="text-lg font-semibold">Ornament Tech Concierge</h2>
                  <div className="text-sm text-white/80 flex items-center gap-2 items-center">
                    <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                    <span>Online • Ready to assist</span>
                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs bg-white/20">
                      <svg className="w-3 h-3" viewBox="0 0 24 24" fill="currentColor">
                        <circle cx="12" cy="12" r="10" />
                      </svg>
                      Engine: {engine === 'unknown' ? 'detecting…' : engine.toUpperCase()}
                    </span>
                    <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs ${mlStatus === 'ok' ? 'bg-green-600' : mlStatus === 'checking' ? 'bg-yellow-500' : 'bg-red-500'}`}>
                      {mlStatus === 'ok' ? 'ML: Online' : mlStatus === 'checking' ? 'ML: Checking...' : 'ML: Offline'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </header>

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gradient-to-b from-gray-50/50 to-white">
            {messages.length === 0 && (
              <div className="text-center py-8">
                <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-r from-primary to-accent flex items-center justify-center">
                  <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <h3 className="text-lg font-semibold text-gray-800 mb-2">Welcome to Ornament Tech!</h3>
                <div className="text-sm text-gray-600 leading-relaxed">
                  I can help you explore our bespoke jewelry process, browse collections, learn about gemstones, 
                  get sizing guidance, and book consultations. What would you like to discover?
                </div>
              </div>
            )}

            {messages.map((m) => (
              <div key={m.id} className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] ${m.role === 'user' ? 'order-2' : 'order-1'}`}>
                  <div className={`rounded-2xl px-4 py-3 ${
                    m.role === 'user' 
                      ? 'bg-gradient-to-r from-primary to-accent text-white ml-4' 
                      : 'bg-white shadow-sm border border-gray-100 text-gray-800 mr-4'
                  }`}>
                    <div className="text-sm leading-relaxed whitespace-pre-wrap">{m.content}</div>
                  </div>
                  <div className={`text-xs text-gray-500 mt-1 px-2 ${m.role === 'user' ? 'text-right' : 'text-left'}`}>
                    {m.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </div>
                </div>
                <div className={`w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center ${
                  m.role === 'user' 
                    ? 'bg-gray-200 order-1 mr-2' 
                    : 'bg-gradient-to-r from-primary to-accent text-white order-2 ml-2'
                }`}>
                  {m.role === 'user' ? (
                    <svg className="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  ) : (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                    </svg>
                  )}
                </div>
              </div>
            ))}
            
            {isTyping && (
              <div className="flex justify-start">
                <div className="max-w-[80%] order-1">
                  <div className="bg-white shadow-sm border border-gray-100 text-gray-800 mr-4 rounded-2xl px-4 py-3">
                    <div className="flex items-center gap-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
                <div className="w-8 h-8 rounded-full flex-shrink-0 flex items-center justify-center bg-gradient-to-r from-primary to-accent text-white order-2 ml-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Enhanced Input Area */}
          <form
            className="border-t border-gray-200 p-4 bg-white"
            onSubmit={(e) => {
              e.preventDefault()
              sendMessage(input)
            }}
          >
            <div className="flex items-end gap-3">
              <div className="flex-1">
                <label htmlFor="ot-chat-input" className="sr-only">
                  Message Ornament Tech
                </label>
                <div className="relative">
                  <input
                    id="ot-chat-input"
                    name="message"
                    placeholder="Ask about rings, necklaces, appointments..."
                    className="w-full rounded-xl border border-gray-200 bg-gray-50 px-4 py-3 text-sm outline-none focus:border-primary focus:bg-white focus:ring-2 focus:ring-primary/20 transition-all duration-200"
                    disabled={isLoading}
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                  />
                  {input.trim() && (
                    <button
                      type="button"
                      onClick={() => setInput("")}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  )}
                </div>
              </div>
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="rounded-xl bg-gradient-to-r from-primary to-accent text-white px-6 py-3 text-sm font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:shadow-lg transform hover:scale-105 transition-all duration-200 flex items-center gap-2"
              >
                {isLoading ? (
                  <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                ) : (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                )}
                <span className="hidden sm:inline">Send</span>
              </button>
            </div>
          </form>
        </div>
      )}

      {/* CSS Animations */}
      <style jsx>{`
        @keyframes slideUp {
          from {
            opacity: 0;
            transform: translateY(20px) scale(0.95);
          }
          to {
            opacity: 1;
            transform: translateY(0) scale(1);
          }
        }
      `}</style>
    </>
  )
}
