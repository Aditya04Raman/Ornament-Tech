export const metadata = { title: "About — Ornament Tech" }

export default function AboutPage() {
  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative">
        <img
          src="/artisan-jeweller-at-work-in-warm-studio.jpg"
          alt="Artisan crafting jewelry in our studio"
          className="h-[70vh] w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-background/50 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto max-w-6xl px-6 py-16">
          <h1 className="font-serif text-5xl md:text-7xl leading-tight text-pretty mb-6">Our Story</h1>
          <p className="mt-3 max-w-3xl text-xl md:text-2xl leading-relaxed opacity-90">
            Where traditional craftsmanship meets cutting-edge technology. 
            Creating jewelry that tells your unique story.
          </p>
        </div>
      </section>

      {/* Story Section */}
      <section className="py-20">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="font-serif text-4xl md:text-5xl mb-6">Crafting Dreams Since 2010</h2>
              <p className="text-lg opacity-90 leading-relaxed mb-6">
                Ornament Tech was born from a simple belief: that every piece of jewelry should be as unique as the person wearing it. 
                We blend time-honored craftsmanship with contemporary design and innovative technology to create pieces that tell your story.
              </p>
              <p className="text-lg opacity-90 leading-relaxed mb-6">
                Our journey began with a small atelier and a big dream. Today, we're proud to have created over 1,200 bespoke pieces, 
                each one a testament to our commitment to excellence and personal service.
              </p>
              <div className="flex items-center gap-4">
                <div className="text-center">
                  <div className="font-serif text-3xl text-primary">15+</div>
                  <div className="text-sm opacity-70">Years Experience</div>
                </div>
                <div className="text-center">
                  <div className="font-serif text-3xl text-primary">1200+</div>
                  <div className="text-sm opacity-70">Pieces Created</div>
                </div>
                <div className="text-center">
                  <div className="font-serif text-3xl text-primary">500+</div>
                  <div className="text-sm opacity-70">Happy Customers</div>
                </div>
              </div>
            </div>
            <div className="rounded-2xl overflow-hidden">
              <img
                src="/artisan-craftsmanship-jewellery.jpg"
                alt="Artisan at work"
                className="w-full h-96 object-cover"
              />
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="py-20 bg-card">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl mb-4">Our Values</h2>
            <p className="text-lg opacity-80 max-w-2xl mx-auto">The principles that guide everything we do</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎨</span>
              </div>
              <h3 className="font-serif text-xl mb-3">Artistry</h3>
              <p className="text-sm opacity-80">Every piece is a work of art, crafted with passion and precision by skilled artisans</p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🤝</span>
              </div>
              <h3 className="font-serif text-xl mb-3">Partnership</h3>
              <p className="text-sm opacity-80">We work closely with you throughout the entire process, ensuring your vision comes to life</p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🌿</span>
              </div>
              <h3 className="font-serif text-xl mb-3">Sustainability</h3>
              <p className="text-sm opacity-80">Ethically sourced materials and responsible practices in everything we create</p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="py-20">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl mb-4">Meet Our Team</h2>
            <p className="text-lg opacity-80">The talented artisans and designers behind every piece</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-32 h-32 rounded-full bg-muted mx-auto mb-4 overflow-hidden">
                <img src="/placeholder-user.jpg" alt="Sarah Chen" className="w-full h-full object-cover" />
              </div>
              <h3 className="font-serif text-xl mb-2">Sarah Chen</h3>
              <p className="text-sm text-primary mb-2">Lead Designer</p>
              <p className="text-xs opacity-80">15+ years crafting bespoke engagement rings</p>
            </div>
            <div className="text-center">
              <div className="w-32 h-32 rounded-full bg-muted mx-auto mb-4 overflow-hidden">
                <img src="/placeholder-user.jpg" alt="Marcus Webb" className="w-full h-full object-cover" />
              </div>
              <h3 className="font-serif text-xl mb-2">Marcus Webb</h3>
              <p className="text-sm text-primary mb-2">Master Goldsmith</p>
              <p className="text-xs opacity-80">Award-winning craftsman specializing in intricate settings</p>
            </div>
            <div className="text-center">
              <div className="w-32 h-32 rounded-full bg-muted mx-auto mb-4 overflow-hidden">
                <img src="/placeholder-user.jpg" alt="Elena Rodriguez" className="w-full h-full object-cover" />
              </div>
              <h3 className="font-serif text-xl mb-2">Elena Rodriguez</h3>
              <p className="text-sm text-primary mb-2">Gemstone Specialist</p>
              <p className="text-xs opacity-80">Expert in sourcing and selecting the finest gemstones</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-card">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="font-serif text-4xl md:text-5xl mb-6">Start Your Story</h2>
          <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
            Ready to create something extraordinary? Let's begin your bespoke journey together.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/appointments"
              className="inline-flex items-center rounded-md bg-primary text-primary-foreground px-8 py-4 text-lg font-medium hover:bg-primary/90 transition-colors"
            >
              Book Consultation
            </a>
            <a
              href="/bespoke-process"
              className="inline-flex items-center rounded-md border-2 border-primary text-primary px-8 py-4 text-lg font-medium hover:bg-primary hover:text-primary-foreground transition-colors"
            >
              Learn Our Process
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}
