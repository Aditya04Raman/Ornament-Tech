import Image from "next/image"
import Link from "next/link"

export const metadata = { title: "Gemstones — Ornament Tech" }

export default function GemstonesPage() {
  const featuredStones = [
    { 
      id: "diamonds",
      title: "Diamonds", 
      body: "The ultimate symbol of eternal love. Understand the 4Cs: cut, color, clarity, and carat weight.",
      details: "From brilliant round cuts to fancy shapes, our diamonds are ethically sourced and certified.",
      image: "/gemstones-macro-editorial.jpg",
      features: ["GIA Certified", "Ethically Sourced", "Full 4C Analysis", "Lifetime Guarantee"]
    },
    { 
      id: "sapphires",
      title: "Sapphires", 
      body: "Durable corundum in a spectrum of magnificent colors from royal blue to pink sunset.",
      details: "Second only to diamonds in hardness, sapphires offer incredible durability and beauty.",
      image: "/gemstone-collection.jpg",
      features: ["Mohs 9 Hardness", "Heat Treatment Options", "Color Varieties", "Ceylon Origins"]
    },
    { 
      id: "emeralds",
      title: "Emeralds", 
      body: "Vibrant green beryl with unique inclusions that tell the story of their formation.",
      details: "Each emerald's garden of inclusions makes it uniquely beautiful and one-of-a-kind.",
      image: "/luxury-jewellery-editorial-hero.jpg",
      features: ["Colombian Sources", "Natural Inclusions", "Oil Treatment", "Vintage Appeal"]
    },
    { 
      id: "rubies",
      title: "Rubies", 
      body: "Rich red corundum prized for its intensity and passionate crimson fire.",
      details: "The birthstone of July, rubies symbolize passion, protection, and prosperity.",
      image: "/diamond-ring-macro-editorial.jpg",
      features: ["Burmese Quality", "Pigeon Blood Red", "Heat Enhancement", "Royal Heritage"]
    },
  ]

  const gemstoneGuide = [
    {
      title: "Understanding Quality",
      content: "Learn how to evaluate gemstone quality through color saturation, clarity, cut precision, and carat weight considerations."
    },
    {
      title: "Care & Maintenance",
      content: "Proper cleaning techniques, storage methods, and professional maintenance to keep your gemstones brilliant for generations."
    },
    {
      title: "Certification",
      content: "Why gemstone certification matters and how our partnership with leading labs ensures authenticity and quality."
    },
    {
      title: "Investment Value",
      content: "Understanding gemstone investment potential, rarity factors, and market trends for informed collecting."
    }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <section className="relative py-16 bg-gradient-to-r from-primary to-accent text-white">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative mx-auto max-w-6xl px-6 text-center">
          <h1 className="text-4xl md:text-5xl font-serif font-bold mb-4">
            Precious Gemstones
          </h1>
          <p className="text-xl md:text-2xl text-white/90 max-w-3xl mx-auto leading-relaxed">
            Discover the world's most coveted gemstones, each carefully selected for exceptional beauty, 
            quality, and provenance in our luxury jewelry creations.
          </p>
        </div>
      </section>

      {/* Featured Gemstones */}
      <section className="mx-auto max-w-6xl px-6 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-serif font-semibold mb-4">Our Signature Gemstones</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Each gemstone in our collection represents the pinnacle of natural beauty and craftsmanship excellence.
          </p>
        </div>

        <div className="grid gap-8 md:grid-cols-2">
          {featuredStones.map((stone) => (
            <div key={stone.id} id={stone.id} className="group">
              <div className="relative overflow-hidden rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-500 bg-white">
                <div className="relative h-64 overflow-hidden">
                  <Image
                    src={stone.image}
                    alt={stone.title}
                    fill
                    className="object-cover group-hover:scale-110 transition-transform duration-700"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent"></div>
                  <div className="absolute bottom-4 left-4 text-white">
                    <h3 className="text-2xl font-serif font-bold">{stone.title}</h3>
                  </div>
                </div>
                
                <div className="p-6">
                  <p className="text-gray-700 mb-4 leading-relaxed">{stone.body}</p>
                  <p className="text-sm text-gray-600 mb-6 leading-relaxed">{stone.details}</p>
                  
                  <div className="grid grid-cols-2 gap-3">
                    {stone.features.map((feature, index) => (
                      <div key={index} className="flex items-center gap-2 text-sm">
                        <div className="w-2 h-2 bg-primary rounded-full"></div>
                        <span className="text-gray-700">{feature}</span>
                      </div>
                    ))}
                  </div>
                  
                  <Link 
                    href={`/gemstones#${stone.id}`}
                    className="mt-6 block w-full bg-gradient-to-r from-primary to-accent text-white py-3 px-6 rounded-lg font-medium hover:shadow-lg transform hover:scale-105 transition-all duration-200 text-center"
                  >
                    Explore {stone.title}
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Gemstone Guide */}
      <section className="bg-gray-50 py-16">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-serif font-semibold mb-4">Gemstone Expertise</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Our comprehensive guide to understanding, selecting, and caring for precious gemstones.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {gemstoneGuide.map((guide, index) => (
              <div key={index} className="bg-white rounded-xl p-6 shadow-sm hover:shadow-lg transition-shadow duration-300">
                <div className="w-12 h-12 bg-gradient-to-r from-primary to-accent rounded-lg flex items-center justify-center mb-4">
                  <span className="text-white font-bold text-lg">{index + 1}</span>
                </div>
                <h3 className="font-semibold text-lg mb-3">{guide.title}</h3>
                <p className="text-sm text-gray-600 leading-relaxed">{guide.content}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="text-3xl font-serif font-semibold mb-4">Ready to Find Your Perfect Gemstone?</h2>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Schedule a private consultation with our gemstone specialists to explore our collection 
            and find the perfect stone for your bespoke jewelry piece.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/appointments"
              className="bg-gradient-to-r from-primary to-accent text-white py-3 px-8 rounded-lg font-medium hover:shadow-lg transform hover:scale-105 transition-all duration-200"
            >
              Book Consultation
            </Link>
            <Link 
              href="/collections"
              className="border border-gray-300 text-gray-700 py-3 px-8 rounded-lg font-medium hover:bg-gray-50 transition-colors duration-200"
            >
              View Collections
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
