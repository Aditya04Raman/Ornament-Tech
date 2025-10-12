export const metadata = { title: "Galleries — Ornament Tech" }

export default function GalleriesPage() {
  const featuredPieces = [
    {
      title: "Sapphire Halo Engagement Ring",
      category: "Engagement Rings",
      image: "/diamond-ring-macro-editorial.jpg",
      description: "A stunning 2.5ct Ceylon sapphire surrounded by brilliant diamonds"
    },
    {
      title: "Rose Gold Wedding Set",
      category: "Wedding Bands",
      image: "/gold-wedding-bands-flatlay-minimal.jpg",
      description: "Matching his and hers bands in warm 18k rose gold"
    },
    {
      title: "Diamond Tennis Necklace",
      category: "Necklaces",
      image: "/gold-necklace-minimal-editorial.jpg",
      description: "Classic elegance with 50 perfectly matched diamonds"
    },
    {
      title: "Emerald Drop Earrings",
      category: "Earrings",
      image: "/gemstones-macro-editorial.jpg",
      description: "Colombian emeralds set in platinum with diamond accents"
    },
    {
      title: "Heritage Bridal Collection",
      category: "Bridal Sets",
      image: "/bridal-jewellery-collection.jpg",
      description: "Vintage-inspired complete bridal jewelry set"
    },
    {
      title: "Art Deco Ring Collection",
      category: "Custom Sets",
      image: "/heritage-jewellery-collection.jpg",
      description: "Bold geometric designs inspired by the 1920s"
    }
  ]

  const categories = [
    { name: "Engagement Rings", count: "120+ pieces", image: "/diamond-ring-macro-editorial.jpg" },
    { name: "Wedding Bands", count: "80+ pieces", image: "/gold-wedding-bands-flatlay-minimal.jpg" },
    { name: "Necklaces", count: "65+ pieces", image: "/gold-necklace-minimal-editorial.jpg" },
    { name: "Earrings", count: "90+ pieces", image: "/gemstones-macro-editorial.jpg" },
    { name: "Bracelets", count: "45+ pieces", image: "/minimal-gold-collection.jpg" },
    { name: "Custom Sets", count: "200+ pieces", image: "/heritage-jewellery-collection.jpg" }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative">
        <img
          src="/editorial-jewellery-gallery.jpg"
          alt="Jewelry Gallery"
          className="h-[80vh] w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/30 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto max-w-6xl px-6 py-20">
          <h1 className="font-serif text-6xl md:text-8xl leading-tight text-white mb-6">Galleries</h1>
          <p className="mt-3 max-w-3xl text-xl md:text-2xl leading-relaxed text-white/90">
            A curated showcase of our finest creations. Each piece tells a unique story of craftsmanship, 
            design excellence, and personal meaning.
          </p>
        </div>
      </section>

      {/* Featured Pieces */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-6">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl mb-4">Featured Masterpieces</h2>
            <p className="text-lg opacity-80 max-w-2xl mx-auto">Our most celebrated creations, each representing the pinnacle of bespoke craftsmanship</p>
          </div>

          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {featuredPieces.map((piece, index) => (
              <div 
                key={piece.title}
                className="group cursor-pointer"
              >
                <div className="relative overflow-hidden rounded-2xl shadow-xl">
                  <img
                    src={piece.image}
                    alt={piece.title}
                    className="h-80 w-full object-cover transition-transform duration-700 group-hover:scale-110"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                  <div className="absolute bottom-0 left-0 right-0 p-6 text-white transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500">
                    <div className="text-xs uppercase tracking-wider text-accent mb-2">{piece.category}</div>
                    <h3 className="font-serif text-xl mb-2">{piece.title}</h3>
                    <p className="text-sm opacity-90 transform translate-y-4 group-hover:translate-y-0 transition-transform duration-500 delay-100">
                      {piece.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Category Browser */}
      <section className="py-20 bg-card">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl mb-4">Browse by Category</h2>
            <p className="text-lg opacity-80">Explore our complete collection organized by jewelry type</p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {categories.map((category) => (
              <div 
                key={category.name}
                className="group relative rounded-xl overflow-hidden cursor-pointer hover:shadow-2xl transition-all duration-500 hover:-translate-y-1"
              >
                <img
                  src={category.image}
                  alt={category.name}
                  className="h-64 w-full object-cover transition-transform duration-700 group-hover:scale-105"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent" />
                <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
                  <h3 className="font-serif text-2xl mb-2 group-hover:text-accent transition-colors">{category.name}</h3>
                  <p className="text-sm opacity-90 mb-3">{category.count}</p>
                  <div className="flex items-center text-sm group-hover:translate-x-2 transition-transform duration-300">
                    <span>View Collection</span>
                    <span className="ml-2">→</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Virtual Tour CTA */}
      <section className="py-20 relative">
        <img
          src="/jewellery-store-interior.jpg"
          alt="Jewelry Store Interior"
          className="absolute inset-0 h-full w-full object-cover"
        />
        <div className="absolute inset-0 bg-black/60" />
        <div className="relative mx-auto max-w-4xl px-6 text-center text-white">
          <h2 className="font-serif text-4xl md:text-5xl mb-6">Experience Our Showroom</h2>
          <p className="text-xl mb-8 max-w-2xl mx-auto opacity-90">
            Take a virtual tour of our flagship boutique or book an appointment to see our collections in person.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/stores"
              className="inline-flex items-center rounded-md bg-accent text-accent-foreground px-8 py-4 text-lg font-medium hover:bg-accent/90 transition-colors"
            >
              Visit Our Stores
            </a>
            <a
              href="/appointments"
              className="inline-flex items-center rounded-md border-2 border-white text-white px-8 py-4 text-lg font-medium hover:bg-white hover:text-black transition-colors"
            >
              Book Private Viewing
            </a>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-background">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="font-serif text-4xl text-primary mb-2">600+</div>
              <div className="text-sm opacity-70">Pieces in Gallery</div>
            </div>
            <div>
              <div className="font-serif text-4xl text-primary mb-2">25+</div>
              <div className="text-sm opacity-70">Award Winners</div>
            </div>
            <div>
              <div className="font-serif text-4xl text-primary mb-2">15</div>
              <div className="text-sm opacity-70">Years Heritage</div>
            </div>
            <div>
              <div className="font-serif text-4xl text-primary mb-2">1200+</div>
              <div className="text-sm opacity-70">Happy Customers</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
