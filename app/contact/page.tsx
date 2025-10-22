"use client"

import { useState } from 'react'

export default function ContactPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsLoading(true)
    setMessage('')

    const formData = new FormData(e.currentTarget)
    const data = {
      name: formData.get('name') as string,
      email: formData.get('email') as string,
      message: formData.get('message') as string,
    }

    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })

      const result = await response.json()

      if (response.ok) {
        setMessage(result.message)
        e.currentTarget.reset()
      } else {
        setMessage(result.error || 'Something went wrong. Please try again.')
      }
    } catch (error) {
      setMessage('Failed to send message. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <section className="mx-auto max-w-3xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Contact</h1>
      <p className="mt-3 opacity-80">We'd love to hear from you.</p>
      
      {message && (
        <div className={`mt-4 p-4 rounded-lg ${message.includes('Thank you') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
          {message}
        </div>
      )}

      <form className="mt-6 grid gap-4" onSubmit={handleSubmit}>
        <input 
          name="name"
          className="rounded-md border border-border bg-background px-3 py-2 text-sm" 
          placeholder="Full name" 
          required 
          disabled={isLoading}
        />
        <input 
          name="email"
          className="rounded-md border border-border bg-background px-3 py-2 text-sm" 
          placeholder="Email" 
          type="email"
          required 
          disabled={isLoading}
        />
        <textarea
          name="message"
          className="rounded-md border border-border bg-background px-3 py-2 text-sm"
          placeholder="Message"
          rows={5}
          required
          disabled={isLoading}
        />
        <button 
          type="submit"
          disabled={isLoading}
          className="rounded-md bg-primary text-primary-foreground px-4 py-2 text-sm w-fit hover:bg-primary/90 transition-colors disabled:opacity-50"
        >
          {isLoading ? 'Sending...' : 'Send Message'}
        </button>
      </form>
    </section>
  )
}
