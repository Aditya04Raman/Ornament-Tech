export const metadata = { title: "Materials — Ornament Tech" }

export default function MaterialsPage() {
  const materials = [
    { 
      title: "Platinum", 
      body: "The ultimate choice for luxury jewelry. Naturally white, hypoallergenic, and incredibly durable. Platinum develops a beautiful patina over time while maintaining its strength.",
      properties: ["Hypoallergenic", "Naturally White", "Extremely Durable", "Develops Patina"],
      image: "/jewellery-materials-macro.jpg"
    },
    { 
      title: "18K Yellow Gold", 
      body: "Classic and timeless with a warm, rich hue. Perfect balance of purity and durability, making it ideal for everyday wear and heirloom pieces.",
      properties: ["Classic Beauty", "Excellent Durability", "Warm Tone", "Traditional Choice"],
      image: "/gold-necklace-minimal-editorial.jpg"
    },
    { 
      title: "18K White Gold", 
      body: "Contemporary elegance with a bright, silvery finish. Rhodium-plated for extra brilliance, though periodic re-plating may be recommended to maintain its lustrous appearance.",
      properties: ["Modern Appeal", "Rhodium Finished", "Bright Appearance", "Versatile Choice"],
      image: "/gold-wedding-bands-flatlay-minimal.jpg"
    },
    { 
      title: "18K Rose Gold", 
      body: "Romantic and distinctive with its beautiful blush tone created by copper alloys. Increasingly popular for its unique warmth and vintage appeal.",
      properties: ["Romantic Tone", "Unique Character", "Vintage Appeal", "Growing Popularity"],
      image: "/minimal-gold-collection.jpg"
    },
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative">
        <img
          src="/jewellery-materials-macro.jpg"
          alt="Precious Metals"
          className="h-[70vh] w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-background/40 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto max-w-6xl px-6 py-16">
          <h1 className="font-serif text-5xl md:text-7xl leading-tight text-pretty mb-6">Precious Materials</h1>
          <p className="mt-3 max-w-3xl text-xl md:text-2xl leading-relaxed opacity-90">
            The finest metals and materials, carefully selected for beauty, durability, and lasting value. 
            Each choice tells part of your story.
          </p>
        </div>
      </section>

      {/* Materials Grid */}
      <section className="py-20">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl mb-4">Our Metal Collection</h2>
            <p className="text-lg opacity-80 max-w-2xl mx-auto">Each metal brings its own character and properties to your bespoke piece</p>
          </div>

          <div className="grid gap-12">
            {materials.map((material, index) => (
              <div key={material.title} className={`flex flex-col lg:flex-row items-center gap-12 ${index % 2 === 1 ? 'lg:flex-row-reverse' : ''}`}>
                <div className="flex-1 lg:max-w-lg">
                  <h3 className="font-serif text-3xl md:text-4xl mb-4">{material.title}</h3>
                  <p className="text-lg opacity-90 leading-relaxed mb-6">{material.body}</p>
                  
                  <div className="grid grid-cols-2 gap-3 mb-6">
                    {material.properties.map((property) => (
                      <div key={property} className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-accent"></div>
                        <span className="text-sm">{property}</span>
                      </div>
                    ))}
                  </div>

                  <a 
                    href="/appointments"
                    className="inline-flex items-center text-primary hover:text-primary/80 transition-colors"
                  >
                    Discuss this material →
                  </a>
                </div>
                <div className="flex-1">
                  <div className="rounded-2xl overflow-hidden shadow-xl">
                    <img
                      src={material.image}
                      alt={material.title}
                      className="w-full h-80 object-cover hover:scale-105 transition-transform duration-700"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Care Guide */}
      <section className="py-20 bg-card">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl mb-4">Caring for Your Metals</h2>
            <p className="text-lg opacity-80">Simple steps to keep your jewelry looking its best</p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center p-6">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🧼</span>
              </div>
              <h3 className="font-serif text-xl mb-3">Regular Cleaning</h3>
              <p className="text-sm opacity-80">Gentle cleaning with warm water and mild soap keeps your pieces brilliant</p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🏠</span>
              </div>
              <h3 className="font-serif text-xl mb-3">Proper Storage</h3>
              <p className="text-sm opacity-80">Individual pouches or compartments prevent scratching and tangling</p>
            </div>
            <div className="text-center p-6">
              <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🔧</span>
              </div>
              <h3 className="font-serif text-xl mb-3">Professional Service</h3>
              <p className="text-sm opacity-80">Annual check-ups ensure settings remain secure and finishes stay fresh</p>
            </div>
          </div>

          <div className="text-center mt-12">
            <a
              href="/care"
              className="inline-flex items-center rounded-md bg-primary text-primary-foreground px-6 py-3 text-lg font-medium hover:bg-primary/90 transition-colors"
            >
              Complete Care Guide
            </a>
          </div>
        </div>
      </section>

      {/* Metal Comparison */}
      <section className="py-20">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl mb-4">Quick Comparison</h2>
            <p className="text-lg opacity-80">Find the perfect metal for your lifestyle and preferences</p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full border-collapse bg-card rounded-xl overflow-hidden shadow-lg">
              <thead>
                <tr className="bg-primary text-primary-foreground">
                  <th className="p-4 text-left">Metal</th>
                  <th className="p-4 text-left">Durability</th>
                  <th className="p-4 text-left">Maintenance</th>
                  <th className="p-4 text-left">Best For</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-border">
                  <td className="p-4 font-medium">Platinum</td>
                  <td className="p-4 text-sm">Highest</td>
                  <td className="p-4 text-sm">Minimal</td>
                  <td className="p-4 text-sm">Engagement rings, daily wear</td>
                </tr>
                <tr className="border-b border-border bg-background/50">
                  <td className="p-4 font-medium">18K Yellow Gold</td>
                  <td className="p-4 text-sm">High</td>
                  <td className="p-4 text-sm">Low</td>
                  <td className="p-4 text-sm">Classic pieces, heirlooms</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="p-4 font-medium">18K White Gold</td>
                  <td className="p-4 text-sm">High</td>
                  <td className="p-4 text-sm">Moderate</td>
                  <td className="p-4 text-sm">Modern designs, versatility</td>
                </tr>
                <tr className="bg-background/50">
                  <td className="p-4 font-medium">18K Rose Gold</td>
                  <td className="p-4 text-sm">High</td>
                  <td className="p-4 text-sm">Low</td>
                  <td className="p-4 text-sm">Romantic pieces, vintage styles</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-card">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="font-serif text-4xl md:text-5xl mb-6">Choose Your Perfect Metal</h2>
          <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
            Not sure which material is right for you? Our experts can guide you through the selection process.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/appointments"
              className="inline-flex items-center rounded-md bg-primary text-primary-foreground px-8 py-4 text-lg font-medium hover:bg-primary/90 transition-colors"
            >
              Book Consultation
            </a>
            <a
              href="/gemstones"
              className="inline-flex items-center rounded-md border-2 border-primary text-primary px-8 py-4 text-lg font-medium hover:bg-primary hover:text-primary-foreground transition-colors"
            >
              Explore Gemstones
            </a>
          </div>
        </div>
      </section>
    </div>
  )
}
