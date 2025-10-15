import { notFound } from 'next/navigation'
import fs from 'fs'
import path from 'path'

interface CollectionPageProps {
  params: Promise<{ collection: string }>
}

interface JewelryItem {
  id: string
  category: string
  type: string
  metal: string
  stone: string
  brand: string
  price: number
  weight: number
  size: number
  [key: string]: any
}

// Helper functions
function formatProductName(text: string): string {
  return text.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
  ).join(' ')
}

function getProductImage(category: string, type: string): string {
  // Map product types to specific jewelry images
  const imageMap: { [key: string]: string } = {
    // Rings
    'ring': '/diamond-ring-macro-editorial.jpg',
    'wedding': '/gold-wedding-bands-flatlay-minimal.jpg',
    'engagement': '/diamond-ring-on-velvet-close-up-luxury-editorial.jpg',
    'statement': '/diamond-ring-macro-editorial.jpg',
    'cocktail': '/gemstones-macro-editorial.jpg',
    'eternity': '/gold-wedding-bands-flatlay-minimal.jpg',
    'solitaire': '/diamond-ring-on-velvet-close-up-luxury-editorial.jpg',
    
    // Necklaces
    'necklace': '/gold-necklace-minimal-editorial.jpg',
    'pendant': '/gold-necklace-minimal-editorial.jpg',
    'chain': '/gold-necklace-minimal-editorial.jpg',
    'choker': '/gold-necklace-minimal-editorial.jpg',
    'lariat': '/gold-necklace-minimal-editorial.jpg',
    
    // Earrings
    'earring': '/editorial-jewellery-gallery.jpg',
    'stud': '/gemstones-macro-editorial.jpg',
    'drop': '/editorial-jewellery-gallery.jpg',
    'hoop': '/editorial-jewellery-gallery.jpg',
    'chandelier': '/heritage-jewellery-collection.jpg',
    
    // Bracelets
    'bracelet': '/gemstone-collection.jpg',
    'bangle': '/minimal-gold-collection.jpg',
    'tennis': '/diamond-ring-macro-editorial.jpg',
    'charm': '/gemstone-collection.jpg',
    'cuff': '/jewellery-materials-macro.jpg',
    
    // Category-based fallbacks
    'bridal': '/bridal-jewellery-collection.jpg',
    'heritage': '/heritage-jewellery-collection.jpg',
    'diamond': '/diamond-ring-macro-editorial.jpg',
    'gemstone': '/gemstones-macro-editorial.jpg',
    'gold': '/minimal-gold-collection.jpg',
    
    // Default
    'default': '/luxury-jewellery-editorial-hero.jpg'
  }
  
  // First try type, then category, then default
  return imageMap[type.toLowerCase()] || 
         imageMap[category.toLowerCase()] || 
         imageMap['default']
}

function getProductDescription(product: JewelryItem): string {
  const metal = formatProductName(product.metal)
  const stone = formatProductName(product.stone)
  const type = formatProductName(product.type)
  const category = formatProductName(product.category)
  const brand = formatProductName(product.brand)
  
  // Create detailed descriptions based on product attributes
  const descriptions = {
    ring: [
      `Exquisite ${type} ring crafted in lustrous ${metal}, featuring stunning ${stone} in a timeless setting. This piece embodies elegance and sophistication.`,
      `Handcrafted ${metal} ${type} ring adorned with premium ${stone}. A perfect symbol of enduring beauty and exceptional craftsmanship.`,
      `Elegant ${type} ring showcasing brilliant ${stone} set in finest ${metal}. Each detail reflects our commitment to luxury and artistry.`,
      `Stunning ${metal} ${type} ring with carefully selected ${stone}. A masterpiece designed to celebrate life's most precious moments.`
    ],
    necklace: [
      `Sophisticated ${type} necklace in premium ${metal}, elegantly enhanced with ${stone} accents. A statement piece for the discerning collector.`,
      `Graceful ${metal} ${type} featuring exquisite ${stone} details. This piece transforms any ensemble with its refined elegance.`,
      `Luxurious ${type} necklace crafted from finest ${metal} and adorned with stunning ${stone}. Where artistry meets timeless design.`,
      `Enchanting ${metal} ${type} with brilliant ${stone} highlights. A piece that speaks to your refined sense of style.`
    ],
    earring: [
      `Captivating ${type} earrings in lustrous ${metal}, beautifully accented with ${stone}. Perfect for adding elegance to any occasion.`,
      `Refined ${metal} ${type} earrings featuring exceptional ${stone}. These pieces frame your face with sophisticated glamour.`,
      `Stunning ${type} earrings crafted in premium ${metal} with brilliant ${stone} details. Timeless elegance for the modern woman.`,
      `Exquisite ${metal} ${type} earrings adorned with carefully selected ${stone}. A perfect blend of luxury and contemporary style.`
    ],
    bracelet: [
      `Elegant ${type} bracelet in finest ${metal}, gracefully enhanced with ${stone} accents. A piece that complements your individual style.`,
      `Sophisticated ${metal} ${type} featuring stunning ${stone} details. This bracelet adds a touch of luxury to your wrist.`,
      `Handcrafted ${type} bracelet in premium ${metal} with exquisite ${stone}. Where traditional craftsmanship meets modern design.`,
      `Beautiful ${metal} ${type} bracelet adorned with brilliant ${stone}. A timeless accessory for the style-conscious individual.`
    ]
  }
  
  // Select appropriate description category
  let descArray = descriptions.ring // default
  if (type.toLowerCase().includes('necklace') || type.toLowerCase().includes('pendant') || type.toLowerCase().includes('chain')) {
    descArray = descriptions.necklace
  } else if (type.toLowerCase().includes('earring') || type.toLowerCase().includes('stud') || type.toLowerCase().includes('drop')) {
    descArray = descriptions.earring
  } else if (type.toLowerCase().includes('bracelet') || type.toLowerCase().includes('bangle')) {
    descArray = descriptions.bracelet
  }
  
  // Use product ID to consistently select description
  const index = parseInt(product.id.replace(/\D/g, '')) % descArray.length
  let description = descArray[index]
  
  // Add brand mention if it's a premium brand
  if (brand && ['Designer', 'Luxury', 'Premium', 'Vintage'].includes(brand)) {
    description += ` From our ${brand} collection.`
  }
  
  return description
}

// Read the actual ML dataset
function getJewelryDataset() {
  try {
    const datasetPath = path.join(process.cwd(), 'ml-chatbot', 'models', 'jewelry_dataset.csv')
    if (fs.existsSync(datasetPath)) {
      const csvData = fs.readFileSync(datasetPath, 'utf-8')
      const lines = csvData.split('\n')
      const headers = lines[0].split(',')
      
      const jewelry = lines.slice(1, -1).map((line, index) => {
        const values = line.split(',')
        if (values.length === headers.length) {
          return {
            id: `ML_${index + 1}`,
            category: values[0]?.replace(/"/g, ''),
            type: values[1]?.replace(/"/g, ''),
            metal: values[2]?.replace(/"/g, ''),
            stone: values[3]?.replace(/"/g, ''),
            weight: parseFloat(values[4]) || 0,
            size: parseFloat(values[5]) || 0,
            brand: values[6]?.replace(/"/g, ''),
            price: parseFloat(values[7]) || 0
          }
        }
        return null
      }).filter(Boolean)
      
      return jewelry
    }
  } catch (error) {
    console.error('Error reading dataset:', error)
  }
  return []
}

// Collection slug mapping
const collectionMapping = {
  'engagement-rings': 'ring',
  'wedding-bands': 'ring',
  'necklaces': 'necklace',
  'earrings': 'earrings',
  'bracelets': 'bracelet',
  'bridal-collection': 'ring',
  'heritage-collection': 'ring'
}

// Collection display data
const collectionsDisplayData = {
  'engagement-rings': {
    name: "Engagement Rings",
    description: "Solitaire classics, vintage-inspired halos, and completely custom designs to mark your unique love story.",
    heroImage: "/diamond-ring-macro-editorial.jpg",
    filterTypes: ['engagement', 'statement', 'cocktail']
  },
  'wedding-bands': {
    name: "Wedding Bands",
    description: "Perfectly paired bands in classic, textured, and shaped styles. Each designed to complement your engagement ring.",
    heroImage: "/gold-wedding-bands-flatlay-minimal.jpg",
    filterTypes: ['wedding', 'eternity']
  },
  'necklaces': {
    name: "Necklaces",
    description: "Delicate pendants to statement pieces, each featuring carefully selected gemstones and precious metals.",
    heroImage: "/gold-necklace-minimal-editorial.jpg",
    filterTypes: ['chain', 'pendant', 'choker', 'tennis', 'statement']
  },
  'earrings': {
    name: "Earrings",
    description: "From elegant studs for everyday wear to dramatic drops for special occasions, crafted with precision.",
    heroImage: "/gemstones-macro-editorial.jpg",
    filterTypes: ['stud', 'drop', 'hoop', 'chandelier', 'huggie']
  },
  'bracelets': {
    name: "Bracelets",
    description: "Elegant bracelets and bangles in precious metals with optional gemstone accents.",
    heroImage: "/placeholder.jpg",
    filterTypes: ['tennis', 'chain', 'bangle', 'charm', 'cuff']
  },
  'bridal-collection': {
    name: "Bridal Collection",
    description: "Complete bridal sets designed to complement each other perfectly for your special day.",
    heroImage: "/bridal-jewellery-collection.jpg",
    filterTypes: ['engagement', 'wedding', 'statement']
  },
  'heritage-collection': {
    name: "Heritage Collection",
    description: "Timeless pieces inspired by classical designs, updated with contemporary craftsmanship.",
    heroImage: "/heritage-jewellery-collection.jpg",
    filterTypes: ['vintage', 'classic', 'luxury']
  }
}

interface CollectionPageProps {
  params: Promise<{ collection: string }>
}

export async function generateStaticParams() {
  return Object.keys(collectionMapping).map((collection) => ({
    collection: collection,
  }))
}

export async function generateMetadata({ params }: CollectionPageProps) {
  const resolvedParams = await params
  const displayData = collectionsDisplayData[resolvedParams.collection as keyof typeof collectionsDisplayData]
  
  if (!displayData) {
    return {
      title: 'Collection Not Found — Ornament Tech'
    }
  }

  return {
    title: `${displayData.name} — Ornament Tech`,
    description: displayData.description
  }
}

export default async function CollectionPage({ params }: CollectionPageProps) {
  const resolvedParams = await params
  const collectionKey = collectionMapping[resolvedParams.collection as keyof typeof collectionMapping]
  const displayData = collectionsDisplayData[resolvedParams.collection as keyof typeof collectionsDisplayData]
  
  if (!collectionKey || !displayData) {
    notFound()
  }

  // Get products from ML dataset
  const allJewelry = getJewelryDataset()
  const categoryProducts = allJewelry
    .filter((item): item is JewelryItem => item !== null && item.category === collectionKey)
    .filter(item => displayData.filterTypes ? displayData.filterTypes.includes(item.type) : true)
    .sort((a, b) => b.price - a.price) // Sort by price descending
    .slice(0, 12) // Limit to 12 items for better performance

  // Calculate metadata from actual data
  const metadata = categoryProducts.length > 0 ? {
    total_products: categoryProducts.length,
    price_range: `$${Math.min(...categoryProducts.map(p => p.price)).toFixed(0)} - $${Math.max(...categoryProducts.map(p => p.price)).toFixed(0)}`,
    popular_metals: [...new Set(categoryProducts.map(p => p.metal))].slice(0, 3),
    average_lead_time: "4-8 weeks"
  } : null

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative">
        <img
          src={displayData.heroImage}
          alt={displayData.name}
          className="h-[70vh] w-full object-cover"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-background/90 via-background/50 to-transparent" />
        <div className="absolute inset-x-0 bottom-0 mx-auto max-w-6xl px-6 py-16">
          <h1 className="font-serif text-5xl md:text-7xl leading-tight text-pretty mb-6">{displayData.name}</h1>
          <p className="mt-3 max-w-3xl text-xl md:text-2xl leading-relaxed opacity-90">
            {displayData.description}
          </p>
          {metadata && (
            <div className="mt-6 flex items-center gap-6 text-lg">
              <span className="font-medium">{metadata.total_products} pieces available</span>
              <span className="text-primary font-medium">{metadata.price_range}</span>
            </div>
          )}
          <div className="mt-8 flex items-center gap-4">
            <a
              href="/appointments"
              className="inline-flex items-center rounded-md bg-accent text-accent-foreground px-6 py-3 text-lg font-medium hover:bg-accent/90 transition-colors"
            >
              Book Consultation
            </a>
            <a href="/bespoke-process" className="inline-flex items-center rounded-md border border-foreground/20 px-6 py-3 text-lg font-medium hover:bg-foreground/5 transition-colors">
              Custom Design
            </a>
          </div>
        </div>
      </section>

      {/* Products Grid */}
      <section className="py-20">
        <div className="mx-auto max-w-7xl px-6">
          <div className="text-center mb-16">
            <h2 className="font-serif text-4xl md:text-5xl mb-4">Our Collection</h2>
            <p className="text-lg opacity-80 max-w-2xl mx-auto">
              {categoryProducts.length > 0 
                ? `Discover ${categoryProducts.length} carefully curated pieces from our ML-trained collection` 
                : "Our curated selection of fine jewelry pieces"
              }
            </p>
          </div>

          {categoryProducts.length > 0 ? (
            <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
              {categoryProducts.map((product: any) => (
                <article 
                  key={product.id} 
                  className="group rounded-2xl overflow-hidden bg-card shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2"
                >
                  <div className="relative overflow-hidden">
                    <img
                      src={getProductImage(product.category, product.type)}
                      alt={`${formatProductName(product.type)} ${formatProductName(product.category)}`}
                      className="h-80 w-full object-cover transition-transform duration-700 group-hover:scale-110"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500" />
                    
                    {/* Wishlist button */}
                    <button 
                      className="absolute top-4 right-4 bg-white/20 backdrop-blur-sm rounded-full p-2 hover:bg-white/30 transition-colors opacity-0 group-hover:opacity-100"
                      aria-label="Add to wishlist"
                    >
                      <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                      </svg>
                    </button>
                    
                    {/* Price overlay */}
                    <div className="absolute bottom-4 left-4 right-4 text-white opacity-0 group-hover:opacity-100 transition-opacity duration-500">
                      <div className="flex justify-between items-end">
                        <div className="text-lg font-semibold">${product.price.toLocaleString()}</div>
                        <div className="text-sm opacity-90">{product.weight.toFixed(1)}g</div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="p-6">
                    <h3 className="font-serif text-2xl mb-3 group-hover:text-primary transition-colors">
                      {formatProductName(product.type)} {formatProductName(product.category)}
                    </h3>
                    <p className="text-sm opacity-80 leading-relaxed mb-4 overflow-hidden" style={{
                      display: '-webkit-box',
                      WebkitLineClamp: 3,
                      WebkitBoxOrient: 'vertical' as const
                    }}>
                      {getProductDescription(product)}
                    </p>
                    
                    {/* Product details */}
                    <div className="mb-6">
                      <div className="text-2xl font-bold text-primary mb-3">${product.price.toLocaleString()}</div>
                      <div className="grid grid-cols-2 gap-2 text-xs opacity-70">
                        <div className="flex items-center gap-1">
                          <span className="w-2 h-2 bg-primary rounded-full"></span>
                          {formatProductName(product.metal)}
                        </div>
                        <div className="flex items-center gap-1">
                          <span className="w-2 h-2 bg-primary rounded-full"></span>
                          {formatProductName(product.stone)}
                        </div>
                        <div className="flex items-center gap-1">
                          <span className="w-2 h-2 bg-primary rounded-full"></span>
                          {formatProductName(product.brand)}
                        </div>
                        <div className="flex items-center gap-1">
                          <span className="w-2 h-2 bg-primary rounded-full"></span>
                          {product.weight.toFixed(1)}g
                        </div>
                      </div>
                    </div>
                    
                    {/* Action buttons */}
                    <div className="space-y-3">
                      <button className="w-full bg-primary text-primary-foreground px-4 py-3 rounded-md text-sm font-medium hover:bg-primary/90 transition-colors flex items-center justify-center gap-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m0 0h8m-8 0a2 2 0 100 4 2 2 0 000-4zm8 0a2 2 0 100 4 2 2 0 000-4z" />
                        </svg>
                        Add to Cart
                      </button>
                      
                      <div className="flex gap-3">
                        <a
                          href="/appointments"
                          className="flex-1 text-center border border-primary text-primary px-4 py-2 rounded-md text-sm font-medium hover:bg-primary hover:text-primary-foreground transition-colors"
                        >
                          Book Viewing
                        </a>
                        <button className="flex-1 text-center border border-primary text-primary px-4 py-2 rounded-md text-sm font-medium hover:bg-primary hover:text-primary-foreground transition-colors">
                          Customize
                        </button>
                      </div>
                      
                      <button className="w-full text-sm text-primary hover:text-primary/80 transition-colors flex items-center justify-center gap-2">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                        </svg>
                        Add to Wishlist
                      </button>
                    </div>
                  </div>
                </article>
              ))}
            </div>
          ) : (
            <div className="text-center py-16">
              <h3 className="text-2xl font-semibold mb-4">Collection Coming Soon</h3>
              <p className="text-lg opacity-80 mb-8">We're curating exceptional pieces for this collection.</p>
              <a
                href="/contact"
                className="inline-flex items-center rounded-md bg-primary text-primary-foreground px-8 py-4 text-lg font-medium hover:bg-primary/90 transition-colors"
              >
                Get Notified
              </a>
            </div>
          )}
        </div>
      </section>

      {/* Process CTA */}
      <section className="py-20 bg-card">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="font-serif text-4xl md:text-5xl mb-6">Don't See What You Love?</h2>
          <p className="text-xl opacity-90 mb-8 max-w-2xl mx-auto">
            Every piece can be customized or we can create something completely unique just for you.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <a
              href="/bespoke-process"
              className="inline-flex items-center rounded-md bg-primary text-primary-foreground px-8 py-4 text-lg font-medium hover:bg-primary/90 transition-colors"
            >
              Start Custom Design
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