export const metadata = { title: "Appointments — Ornament Tech" }

export default function AppointmentsPage() {
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
              <form className="space-y-6">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">First Name *</label>
                    <input 
                      className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" 
                      placeholder="John" 
                      required
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Last Name *</label>
                    <input 
                      className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" 
                      placeholder="Smith" 
                      required
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Email Address *</label>
                  <input 
                    type="email"
                    className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" 
                    placeholder="john@example.com" 
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Phone Number</label>
                  <input 
                    type="tel"
                    className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" 
                    placeholder="+44 20 1234 5678" 
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Consultation Type *</label>
                  <select className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent">
                    <option>In-Person Consultation</option>
                    <option>Virtual Video Call</option>
                    <option>Phone Consultation</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Preferred Location</label>
                  <select className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent">
                    <option>London Studio</option>
                    <option>Cambridge Boutique</option>
                    <option>Virtual Appointment</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Project Type</label>
                  <select className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent">
                    <option>Engagement Ring</option>
                    <option>Wedding Bands</option>
                    <option>Custom Necklace</option>
                    <option>Earrings</option>
                    <option>Bracelet</option>
                    <option>Ring Redesign</option>
                    <option>Other</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Budget Range</label>
                  <select className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent">
                    <option>£1,000 - £3,000</option>
                    <option>£3,000 - £5,000</option>
                    <option>£5,000 - £10,000</option>
                    <option>£10,000 - £20,000</option>
                    <option>£20,000+</option>
                    <option>Prefer to discuss</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Tell us about your project</label>
                  <textarea
                    className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent"
                    placeholder="Share your vision, inspiration, or any specific requirements..."
                    rows={4}
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Preferred Date/Time</label>
                  <input 
                    type="datetime-local"
                    className="w-full rounded-md border border-border bg-background px-4 py-3 text-sm focus:ring-2 focus:ring-primary focus:border-transparent" 
                  />
                </div>

                <button className="w-full rounded-md bg-primary text-primary-foreground px-6 py-4 text-lg font-medium hover:bg-primary/90 transition-colors">
                  Request Consultation
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
