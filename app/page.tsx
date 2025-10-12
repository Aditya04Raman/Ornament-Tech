export default function HomePage() {
  return (
    <main>
      {/* Hero */}
      <section className="relative">
        <img
          src="/diamond-ring-on-velvet-close-up-luxury-editorial.jpg"
          alt="Diamond engagement ring on velvet"
          className="h-[60vh] md:h-[72vh] w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-background/40 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto max-w-6xl px-6 py-10 md:py-14">
          <h1 className="font-serif text-4xl md:text-6xl leading-tight text-pretty">Ornament Tech</h1>
          <p className="mt-3 max-w-2xl text-pretty leading-relaxed opacity-85">
            Bespoke jewellery, crafted with care. Editorial presentation, high‑resolution imagery, and an AI concierge
            to guide your journey.
          </p>
          <div className="mt-6 flex items-center gap-3">
            <a
              href="/appointments"
              className="inline-flex items-center rounded-md bg-accent text-accent-foreground px-4 py-2 text-sm"
            >
              Book a Consultation
            </a>
            <a href="/collections" className="inline-flex items-center rounded-md border px-4 py-2 text-sm">
              Explore Collections
            </a>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="px-6 py-12 bg-background">
        <div className="mx-auto max-w-6xl">
          <div className="grid gap-8 md:grid-cols-3 text-center">
            <div>
              <div className="font-serif text-4xl md:text-5xl text-primary">15+</div>
              <div className="mt-2 text-sm opacity-70">Years of Experience</div>
            </div>
            <div>
              <div className="font-serif text-4xl md:text-5xl text-primary">500+</div>
              <div className="mt-2 text-sm opacity-70">Happy Customers</div>
            </div>
            <div>
              <div className="font-serif text-4xl md:text-5xl text-primary">1200+</div>
              <div className="mt-2 text-sm opacity-70">Pieces Created</div>
            </div>
          </div>
        </div>
      </section>

      {/* Craftsmanship Story */}
      <section className="px-6 py-14 md:py-20 bg-card">
        <div className="mx-auto grid max-w-6xl gap-8 md:grid-cols-2">
          <div className="rounded-lg overflow-hidden">
            <img
              src="/artisan-jeweller-at-work-in-warm-studio.jpg"
              alt="An artisan jeweller handcrafting a ring"
              className="h-full w-full object-cover"
            />
          </div>
          <div className="self-center">
            <h2 className="font-serif text-3xl md:text-4xl text-pretty">Bespoke Craft, From Sketch to Sparkle</h2>
            <p className="mt-3 leading-relaxed opacity-90">
              Begin with a conversation and a sketch. We source stones ethically, refine the design together, and
              hand‑craft your piece in our studio.
            </p>
            <div className="mt-5">
              <a
                href="/bespoke-process"
                className="inline-flex items-center text-sm underline decoration-1 underline-offset-4"
              >
                Discover the Bespoke Process
              </a>
            </div>
          </div>
        </div>
      </section>

      {/* Collections */}
      <section className="px-6 py-14 md:py-20">
        <div className="mx-auto max-w-6xl">
          <header className="mb-8">
            <h2 className="font-serif text-3xl md:text-4xl">Curated Collections</h2>
            <p className="mt-2 opacity-85">Engagement rings, wedding bands, and timeless signature pieces.</p>
          </header>
          <div className="grid gap-6 md:grid-cols-3">
            {[
              {
                title: "Engagement",
                img: "/diamond-ring-macro-editorial.jpg",
                href: "/collections#engagement",
              },
              {
                title: "Wedding Bands",
                img: "/gold-wedding-bands-flatlay-minimal.jpg",
                href: "/collections#wedding-bands",
              },
              {
                title: "Necklaces",
                img: "/gold-necklace-minimal-editorial.jpg",
                href: "/collections#necklaces",
              },
            ].map((c) => (
              <a key={c.title} href={c.href} className="group rounded-lg overflow-hidden border bg-card">
                <img
                  src={c.img || "/placeholder.svg"}
                  alt={c.title}
                  className="h-60 w-full object-cover transition duration-300 group-hover:scale-[1.02]"
                />
                <div className="p-4">
                  <h3 className="text-base font-medium">{c.title}</h3>
                  <p className="mt-1 text-sm opacity-80">Explore designs and made‑to‑order options.</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="px-6 py-14 md:py-20 bg-card">
        <div className="mx-auto max-w-6xl">
          <header className="text-center mb-12">
            <h2 className="font-serif text-3xl md:text-4xl">What Our Customers Say</h2>
          </header>
          <div className="grid gap-8 md:grid-cols-3">
            <div className="bg-background rounded-lg p-6">
              <div className="flex mb-3">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-accent">★</span>
                ))}
              </div>
              <p className="text-sm opacity-90 mb-4">"Absolutely stunning ring! The bespoke process was so personal and the final piece exceeded all expectations."</p>
              <div className="text-xs opacity-70">— Sarah M.</div>
            </div>
            <div className="bg-background rounded-lg p-6">
              <div className="flex mb-3">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-accent">★</span>
                ))}
              </div>
              <p className="text-sm opacity-90 mb-4">"Professional service from start to finish. They truly understood our vision and brought it to life perfectly."</p>
              <div className="text-xs opacity-70">— James & Emma K.</div>
            </div>
            <div className="bg-background rounded-lg p-6">
              <div className="flex mb-3">
                {[...Array(5)].map((_, i) => (
                  <span key={i} className="text-accent">★</span>
                ))}
              </div>
              <p className="text-sm opacity-90 mb-4">"The quality is exceptional and the AI concierge made the whole experience so smooth and informative."</p>
              <div className="text-xs opacity-70">— Michael R.</div>
            </div>
          </div>
        </div>
      </section>

      {/* Appointment CTA */}
      <section className="px-6 pb-16 md:pb-24">
        <div className="mx-auto max-w-6xl rounded-xl border bg-card p-6 md:p-8">
          <h2 className="font-serif text-2xl md:text-3xl">Ready to begin?</h2>
          <p className="mt-2 leading-relaxed opacity-90">
            Chat with our concierge or book a consultation to discuss stones, metals, and design details.
          </p>
          <div className="mt-5 flex items-center gap-3">
            <a
              href="/appointments"
              className="inline-flex items-center rounded-md bg-primary text-primary-foreground px-4 py-2 text-sm"
            >
              Book Appointment
            </a>
            <a href="/gemstones" className="inline-flex items-center rounded-md border px-4 py-2 text-sm">
              Learn about Gemstones
            </a>
          </div>
        </div>
      </section>
    </main>
  )
}
