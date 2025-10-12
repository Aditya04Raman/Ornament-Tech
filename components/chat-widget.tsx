"use client"

import { useState } from "react"
import { useChat } from "@ai-sdk/react"
import { DefaultChatTransport } from "ai"

export default function ChatWidget() {
  const [open, setOpen] = useState(false)

  const { messages, sendMessage, status } = useChat({
    transport: new DefaultChatTransport({ api: "/api/chat" }),
  })

  return (
    <>
      {/* Toggle Button */}
      <button
        aria-label="Open Ornament Tech chat"
        onClick={() => setOpen((v) => !v)}
        className="fixed bottom-6 right-6 z-40 rounded-full px-4 py-3 bg-primary text-primary-foreground shadow-lg border border-border"
      >
        {open ? "Close Chat" : "Chat with us"}
      </button>

      {/* Panel */}
      {open && (
        <div
          role="dialog"
          aria-modal="true"
          className="fixed bottom-24 right-6 z-40 w-[22rem] max-w-[90vw] rounded-lg border border-border bg-card text-foreground shadow-xl flex flex-col"
        >
          <header className="px-4 py-3 border-b border-border">
            <h2 className="text-sm font-medium text-pretty">Ornament Tech Concierge</h2>
            <p className="text-xs opacity-70">
              Ask about our bespoke process, gemstones, sizing, galleries, or bookings.
            </p>
          </header>

          <div className="flex-1 overflow-y-auto p-3 space-y-3">
            {messages.length === 0 && (
              <div className="text-sm opacity-70">
                Hello! How can I help you today? I can guide you through bespoke consultations, materials and gemstone
                choices, size guidance, and appointment booking.
              </div>
            )}

            {messages.map((m) => (
              <div key={m.id} className="text-sm">
                <div className="mb-1 font-semibold">{m.role === "user" ? "You" : "Ornament Tech"}</div>
                <div className="rounded-md border border-border bg-background p-2 leading-relaxed">
                  {m.parts.map((part, idx) => {
                    if (part.type === "text") return <div key={idx}>{part.text}</div>
                    return null
                  })}
                </div>
              </div>
            ))}
          </div>

          <form
            className="border-t border-border p-2 flex items-center gap-2"
            onSubmit={(e) => {
              e.preventDefault()
              const inputEl = e.currentTarget.elements.namedItem("message") as HTMLInputElement
              const value = inputEl.value.trim()
              if (!value) return
              sendMessage({ text: value })
              inputEl.value = ""
            }}
          >
            <label htmlFor="ot-chat-input" className="sr-only">
              Message Ornament Tech
            </label>
            <input
              id="ot-chat-input"
              name="message"
              placeholder="Type your message…"
              className="flex-1 rounded-md border border-border bg-background px-3 py-2 text-sm outline-none"
              disabled={status === "in_progress"}
            />
            <button
              type="submit"
              className="rounded-md bg-primary text-primary-foreground px-3 py-2 text-sm"
              disabled={status === "in_progress"}
            >
              Send
            </button>
          </form>
        </div>
      )}
    </>
  )
}
