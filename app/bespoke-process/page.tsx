export const metadata = { title: "Bespoke Process — Ornament Tech" }

export default function BespokeProcessPage() {
  const steps = [
    { 
      title: "Consultation", 
      body: "Share your vision and story with our designers. We'll discuss your budget, timeline, and unique inspirations to create the perfect foundation for your piece.",
      icon: "💬",
      image: "/jewellery-boutique-appointment.jpg"
    },
    { 
      title: "Design", 
      body: "Watch your dreams take shape through hand-drawn sketches and 3D CAD models. We'll refine every detail together until the design is perfect.",
      icon: "✨",
      image: "/artisan-bench-bespoke-jewellery-process.jpg"
    },
    { 
      title: "Craft", 
      body: "Our master craftspeople bring your design to life using traditional techniques and modern precision. Every piece is handmade with exceptional attention to detail.",
      icon: "🔨",
      image: "/artisan-craftsmanship-jewellery.jpg"
    },
    { 
      title: "Delivery", 
      body: "Your completed masterpiece undergoes rigorous quality checks before being presented in our signature packaging. The moment you've been waiting for.",
      icon: "🎁",
      image: "/diamond-ring-on-velvet-close-up-luxury-editorial.jpg"
    },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-b from-background to-card">
        <div className="absolute inset-0 bg-[url('/studio-portrait-editorial.jpg')] bg-cover bg-center opacity-10"></div>
        <div className="relative mx-auto max-w-6xl px-6 py-20 text-center">
          <h1 className="font-serif text-5xl md:text-7xl text-pretty mb-6">Your Bespoke Journey</h1>
          <p className="text-xl md:text-2xl opacity-90 max-w-3xl mx-auto leading-relaxed">
            From the spark of an idea to the perfect piece that tells your story. 
            Experience the magic of true bespoke craftsmanship.
          </p>
          <div className="mt-8">
            <a
              href="/appointments"
              className="inline-flex items-center rounded-md bg-primary text-primary-foreground px-8 py-4 text-lg font-medium hover:bg-primary/90 transition-colors"
            >
              Start Your Journey
            </a>
          </div>
        </div>
      </section>

      {/* Process Steps */}
      <section className="py-20">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl mb-4">The Four Pillars of Bespoke</h2>
            <p className="text-lg opacity-80 max-w-2xl mx-auto">Each step is carefully orchestrated to ensure your vision becomes reality</p>
          </div>
          
          <div className="space-y-16">
            {steps.map((step, index) => (
              <div key={step.title} className={`flex flex-col lg:flex-row items-center gap-12 ${index % 2 === 1 ? 'lg:flex-row-reverse' : ''}`}>
                <div className="flex-1 lg:max-w-lg">
                  <div className="flex items-center gap-4 mb-6">
                    <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center text-2xl">
                      {step.icon}
                    </div>
                    <div>
                      <div className="text-sm text-primary font-medium">Step {index + 1}</div>
                      <h3 className="font-serif text-3xl md:text-4xl">{step.title}</h3>
                    </div>
                  </div>
                  <p className="text-lg opacity-90 leading-relaxed mb-6">{step.body}</p>
                  <div className="flex items-center gap-2 text-sm text-primary">
                    <span>Learn more about this step</span>
                    <span>→</span>
                  </div>
                </div>
                <div className="flex-1">
                  <div className="rounded-2xl overflow-hidden shadow-2xl">
                    <img
                      src={step.image}
                      alt={`${step.title} process`}
                      className="w-full h-80 object-cover hover:scale-105 transition-transform duration-700"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Timeline */}
      <section className="py-20 bg-card">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="font-serif text-4xl mb-8">Typical Timeline</h2>
          <div className="grid md:grid-cols-4 gap-8">
            <div className="relative">
              <div className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center mx-auto mb-4 text-lg font-semibold">1</div>
              <h3 className="font-medium mb-2">Week 1</h3>
              <p className="text-sm opacity-80">Initial consultation and design brief</p>
            </div>
            <div className="relative">
              <div className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center mx-auto mb-4 text-lg font-semibold">2</div>
              <h3 className="font-medium mb-2">Weeks 2-3</h3>
              <p className="text-sm opacity-80">Design development and approval</p>
            </div>
            <div className="relative">
              <div className="w-12 h-12 rounded-full bg-primary text-primary-foreground flex items-center justify-center mx-auto mb-4 text-lg font-semibold">3</div>
              <h3 className="font-medium mb-2">Weeks 4-8</h3>
              <p className="text-sm opacity-80">Handcrafting your piece</p>
            </div>
            <div className="relative">
              <div className="w-12 h-12 rounded-full bg-accent text-accent-foreground flex items-center justify-center mx-auto mb-4 text-lg font-semibold">✓</div>
              <h3 className="font-medium mb-2">Week 9</h3>
              <p className="text-sm opacity-80">Quality check and delivery</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="font-serif text-4xl md:text-5xl mb-6">Ready to Begin Your Story?</h2>
          <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
            Let's create something extraordinary together. Book your consultation and take the first step toward your perfect piece.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/appointments"
              className="inline-flex items-center rounded-md bg-primary text-primary-foreground px-8 py-4 text-lg font-medium hover:bg-primary/90 transition-colors"
            >
              Book Consultation
            </a>
            <a
              href="/galleries"
              className="inline-flex items-center rounded-md border-2 border-primary text-primary px-8 py-4 text-lg font-medium hover:bg-primary hover:text-primary-foreground transition-colors"
            >
              View Our Work
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}
