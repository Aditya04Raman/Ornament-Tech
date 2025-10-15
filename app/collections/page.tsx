export const metadata = { title: "Collections — Ornament Tech" }

export default function CollectionsPage() {
  const collections = [
    { 
      name: "Engagement Rings", 
      slug: "engagement-rings",
      desc: "Solitaire classics, vintage-inspired halos, and completely custom designs to mark your unique love story.",
      image: "/diamond-ring-macro-editorial.jpg",
      pieces: "50+ designs",
      startingPrice: "From £2,500"
    },
    { 
      name: "Wedding Bands", 
      slug: "wedding-bands",
      desc: "Perfectly paired bands in classic, textured, and shaped styles. Each designed to complement your engagement ring.",
      image: "/gold-wedding-bands-flatlay-minimal.jpg",
      pieces: "40+ designs",
      startingPrice: "From £800"
    },
    { 
      name: "Necklaces", 
      slug: "necklaces",
      desc: "Delicate pendants to statement pieces, each featuring carefully selected gemstones and precious metals.",
      image: "/gold-necklace-minimal-editorial.jpg",
      pieces: "35+ designs",
      startingPrice: "From £1,200"
    },
    { 
      name: "Earrings", 
      slug: "earrings",
      desc: "From elegant studs for everyday wear to dramatic drops for special occasions, crafted with precision.",
      image: "/gemstones-macro-editorial.jpg",
      pieces: "45+ designs",
      startingPrice: "From £600"
    },
    { 
      name: "Bridal Collection", 
      slug: "bridal-collection",
      desc: "Complete bridal sets designed to complement each other perfectly for your special day.",
      image: "/bridal-jewellery-collection.jpg",
      pieces: "25+ sets",
      startingPrice: "From £3,500"
    },
    { 
      name: "Heritage Collection", 
      slug: "heritage-collection",
      desc: "Timeless pieces inspired by classical designs, updated with contemporary craftsmanship.",
      image: "/heritage-jewellery-collection.jpg",
      pieces: "30+ designs",
      startingPrice: "From £1,800"
    },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative">
        <img
          src="/editorial-jewellery-gallery.jpg"
          alt="Jewelry Collection"
          className="h-[70vh] w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-background/50 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto max-w-6xl px-6 py-16">
          <h1 className="font-serif text-5xl md:text-7xl leading-tight text-pretty mb-6">Curated Collections</h1>
          <p className="mt-3 max-w-3xl text-xl md:text-2xl leading-relaxed opacity-90">
            Discover our signature collections, each piece thoughtfully designed and meticulously crafted. 
            From timeless classics to contemporary statements.
          </p>
          <div className="mt-8 flex items-center gap-4">
            <a
              href="/appointments"
              className="inline-flex items-center rounded-md bg-accent text-accent-foreground px-6 py-3 text-lg font-medium hover:bg-accent/90 transition-colors"
            >
              Book Private Viewing
            </a>
            <a href="/galleries" className="inline-flex items-center rounded-md border border-foreground/20 px-6 py-3 text-lg font-medium hover:bg-foreground/5 transition-colors">
              View Gallery
            </a>
          </div>
        </div>
      </section>

      {/* Collections Grid */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-6">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl mb-4">Our Signature Collections</h2>
            <p className="text-lg opacity-80 max-w-2xl mx-auto">Each collection tells a story, crafted for life's most precious moments</p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {collections.map((collection, index) => (
              <article 
                key={collection.name} 
                className="group rounded-2xl overflow-hidden bg-card shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2"
              >
                <div className="relative overflow-hidden">
                  <img
                    src={collection.image}
                    alt={collection.name}
                    className="h-80 w-full object-cover transition-transform duration-700 group-hover:scale-110"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                  <div className="absolute bottom-4 left-4 right-4 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                    <div className="flex justify-between items-end">
                      <div>
                        <div className="text-sm font-medium">{collection.pieces}</div>
                        <div className="text-xs opacity-90">{collection.startingPrice}</div>
                      </div>
                      <a
                        href={`/collections/${collection.slug}`}
                        className="bg-white/20 backdrop-blur-sm rounded-full p-2 hover:bg-white/30 transition-colors"
                      >
                        <span className="text-lg">→</span>
                      </a>
                    </div>
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="font-serif text-2xl mb-3 group-hover:text-primary transition-colors">{collection.name}</h3>
                  <p className="text-sm opacity-80 leading-relaxed mb-4">{collection.desc}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-primary font-medium">{collection.pieces}</span>
                    <a 
                      href={`/collections/${collection.slug}`}
                      className="text-sm text-primary hover:underline"
                    >
                      Explore Collection →
                    </a>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-card">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div className="p-6">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">💎</span>
              </div>
              <h3 className="font-serif text-xl mb-3">Ethically Sourced</h3>
              <p className="text-sm opacity-80">Every gemstone and metal is responsibly sourced with full traceability</p>
            </div>
            <div className="p-6">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🏆</span>
              </div>
              <h3 className="font-serif text-xl mb-3">Award Winning</h3>
              <p className="text-sm opacity-80">Recognition for exceptional craftsmanship and innovative design</p>
            </div>
            <div className="p-6">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🛡️</span>
              </div>
              <h3 className="font-serif text-xl mb-3">Lifetime Guarantee</h3>
              <p className="text-sm opacity-80">Comprehensive warranty covering craftsmanship and materials</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="font-serif text-4xl md:text-5xl mb-6">Create Your Perfect Piece</h2>
          <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
            Don't see exactly what you're looking for? Let's create something completely unique together.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/bespoke-process"
              className="inline-flex items-center rounded-md bg-primary text-primary-foreground px-8 py-4 text-lg font-medium hover:bg-primary/90 transition-colors"
            >
              Start Bespoke Journey
            </a>
            <a
              href="/contact"
              className="inline-flex items-center rounded-md border-2 border-primary text-primary px-8 py-4 text-lg font-medium hover:bg-primary hover:text-primary-foreground transition-colors"
            >
              Speak to Designer
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}
