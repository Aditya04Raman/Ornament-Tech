"use client"

import { useState } from 'react'

export default function AppointmentsPage() {
  const [isLoading, setIsLoading] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setIsLoading(true)
    setMessage('')

    const formData = new FormData(e.currentTarget)
    const data = {
      firstName: formData.get('firstName') as string,
      lastName: formData.get('lastName') as string,
      email: formData.get('email') as string,
      phone: formData.get('phone') as string,
      consultationType: formData.get('consultationType') as string,
      location: formData.get('location') as string,
      projectType: formData.get('projectType') as string,
      budgetRange: formData.get('budgetRange') as string,
      projectDescription: formData.get('projectDescription') as string,
      preferredDateTime: formData.get('preferredDateTime') as string,
    }

    try {
      const response = await fetch('/api/appointments', {
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
      setMessage('Failed to book appointment. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative">
        <img
          src="/jewellery-boutique-appointment.jpg"
          alt="Jewelry Consultation"
          className="h-[60vh] w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-background/50 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto max-w-6xl px-6 py-12">
          <h1 className="font-serif text-5xl md:text-6xl leading-tight text-pretty mb-4">Book Your Consultation</h1>
          <p className="mt-3 max-w-2xl text-lg md:text-xl leading-relaxed opacity-90">
            Begin your bespoke journey with a personal consultation. 
            Available in-person at our studios or virtually from anywhere in the world.
          </p>
        </div>
      </section>

      <section className="py-20">
        <div className="mx-auto max-w-4xl px-6">
          <div className="grid md:grid-cols-2 gap-12">
            {/* Booking Form */}
            <div>
              <h2 className="font-serif text-3xl mb-6">Schedule Your Appointment</h2>
              
              {message && (
                <div className={`mb-6 p-4 rounded-lg ${message.includes('received') ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'}`}>
                  {message}
                </div>
              )}

              <form className="space-y-6" onSubmit={handleSubmit}>
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">First Name *</label>
                    <input 
                      name="firstName"
                      className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" 
                      placeholder="John" 
                      required
                      disabled={isLoading}
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Last Name *</label>
                    <input 
                      name="lastName"
                      className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" 
                      placeholder="Smith" 
                      required
                      disabled={isLoading}
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Email Address *</label>
                  <input 
                    name="email"
                    type="email"
                    className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" 
                    placeholder="john@example.com" 
                    required
                    disabled={isLoading}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Phone Number</label>
                  <input 
                    name="phone"
                    type="tel"
                    className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" 
                    placeholder="+44 20 1234 5678" 
                    disabled={isLoading}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Consultation Type *</label>
                  <select name="consultationType" className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" required disabled={isLoading}>
                    <option value="">Select consultation type</option>
                    <option value="In-Person Consultation">In-Person Consultation</option>
                    <option value="Virtual Video Call">Virtual Video Call</option>
                    <option value="Phone Consultation">Phone Consultation</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Preferred Location</label>
                  <select name="location" className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" disabled={isLoading}>
                    <option value="">Select location</option>
                    <option value="London Studio">London Studio</option>
                    <option value="Cambridge Boutique">Cambridge Boutique</option>
                    <option value="Virtual Appointment">Virtual Appointment</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Project Type</label>
                  <select name="projectType" className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" disabled={isLoading}>
                    <option value="">Select project type</option>
                    <option value="Engagement Ring">Engagement Ring</option>
                    <option value="Wedding Bands">Wedding Bands</option>
                    <option value="Custom Necklace">Custom Necklace</option>
                    <option value="Earrings">Earrings</option>
                    <option value="Bracelet">Bracelet</option>
                    <option value="Ring Redesign">Ring Redesign</option>
                    <option value="Other">Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Budget Range</label>
                  <select name="budgetRange" className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" disabled={isLoading}>
                    <option value="">Select budget range</option>
                    <option value="£1,000 - £3,000">£1,000 - £3,000</option>
                    <option value="£3,000 - £5,000">£3,000 - £5,000</option>
                    <option value="£5,000 - £10,000">£5,000 - £10,000</option>
                    <option value="£10,000 - £20,000">£10,000 - £20,000</option>
                    <option value="£20,000+">£20,000+</option>
                    <option value="Prefer to discuss">Prefer to discuss</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Tell us about your project</label>
                  <textarea
                    name="projectDescription"
                    className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="Share your vision, inspiration, or any specific requirements..."
                    rows={4}
                    disabled={isLoading}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Preferred Date/Time</label>
                  <input 
                    name="preferredDateTime"
                    type="datetime-local"
                    className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" 
                    disabled={isLoading}
                  />
                </div>

                <button 
                  type="submit"
                  disabled={isLoading}
                  className="w-full rounded-md bg-primary text-primary-foreground px-6 py-4 text-lg font-medium hover:bg-primary/90 transition-colors disabled:opacity-50"
                >
                  {isLoading ? 'Requesting...' : 'Request Consultation'}
                </button>
              </form>
              
              <div className="mt-6 p-4 bg-card rounded-lg">
                <p className="text-sm opacity-70">
                  <strong>Quick questions?</strong> Try our AI chat assistant in the bottom-right corner for instant help.
                </p>
              </div>
            </div>

            {/* Information Sidebar */}
            <div className="space-y-8">
              <div>
                <h3 className="font-serif text-2xl mb-4">What to Expect</h3>
                <div className="space-y-4">
                  <div className="flex gap-3">
                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-sm">1</span>
                    </div>
                    <div>
                      <h4 className="font-medium mb-1">Discovery Session</h4>
                      <p className="text-sm opacity-80">We'll discuss your vision, lifestyle, and preferences to understand exactly what you're looking for.</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-sm">2</span>
                    </div>
                    <div>
                      <h4 className="font-medium mb-1">Design Exploration</h4>
                      <p className="text-sm opacity-80">View our collections, explore materials, and begin sketching your unique design concept.</p>
                    </div>
                  </div>
                  <div className="flex gap-3">
                    <div className="w-8 h-8 rounded-full bg-primary/10 flex items-center justify-center flex-shrink-0 mt-1">
                      <span className="text-sm">3</span>
                    </div>
                    <div>
                      <h4 className="font-medium mb-1">Next Steps</h4>
                      <p className="text-sm opacity-80">Receive a detailed proposal with timeline, pricing, and the path forward for your bespoke piece.</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="bg-card p-6 rounded-xl">
                <h3 className="font-serif text-xl mb-4">Contact Information</h3>
                <div className="space-y-3 text-sm">
                  <div>
                    <strong>London Studio</strong><br />
                    69 Regent's Park Road<br />
                    Primrose Hill, London NW1 8UY<br />
                    <a href="tel:02081549500" className="text-primary hover:underline">020 8154 9500</a>
                  </div>
                  <div>
                    <strong>Cambridge Boutique</strong><br />
                    6/7 Green Street<br />
                    Cambridge CB2 3JU<br />
                    <a href="tel:01223461333" className="text-primary hover:underline">01223 461333</a>
                  </div>
                  <div>
                    <strong>Email</strong><br />
                    <a href="mailto:hello@ornamenttech.com" className="text-primary hover:underline">hello@ornamenttech.com</a>
                  </div>
                </div>
              </div>

              <div className="bg-accent/10 p-6 rounded-xl">
                <h3 className="font-serif text-xl mb-4">Free Consultation</h3>
                <p className="text-sm opacity-90 mb-4">
                  All initial consultations are complimentary with no obligation. 
                  We believe in building relationships first, beautiful jewelry second.
                </p>
                <div className="text-sm">
                  <strong>Typical consultation duration:</strong> 60-90 minutes
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
