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
}

// Helper functions
function formatProductName(text: string): string {
  return text.split('_').map(word => 
    word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()
  ).join(' ')
}

function getProductImage(category: string, type: string): string {
  // Map product types to specific jewelry images with absolute paths
  const imageMap: { [key: string]: string } = {
    // Ring types
    'statement': '/diamond-ring-macro-editorial.jpg',
    'cocktail': '/gemstones-macro-editorial.jpg', 
    'engagement': '/diamond-ring-on-velvet-close-up-luxury-editorial.jpg',
    'eternity': '/gold-wedding-bands-flatlay-minimal.jpg',
    'wedding': '/gold-wedding-bands-flatlay-minimal.jpg',
    
    // Necklace types
    'chain': '/gold-necklace-minimal-editorial.jpg',
    'tennis': '/heritage-jewellery-collection.jpg',
    'choker': '/gold-necklace-minimal-editorial.jpg', 
    'pendant': '/gold-necklace-minimal-editorial.jpg',
    
    // Earring types
    'chandelier': '/heritage-jewellery-collection.jpg',
    'hoop': '/editorial-jewellery-gallery.jpg',
    'drop': '/editorial-jewellery-gallery.jpg',
    'huggie': '/editorial-jewellery-gallery.jpg',
    'stud': '/gemstones-macro-editorial.jpg',
    
    // Bracelet types
    'charm': '/gemstone-collection.jpg',
    'bangle': '/minimal-gold-collection.jpg',
    'cuff': '/jewellery-materials-macro.jpg',
    
    // Category fallbacks
    'ring': '/diamond-ring-macro-editorial.jpg',
    'necklace': '/gold-necklace-minimal-editorial.jpg',
    'earrings': '/editorial-jewellery-gallery.jpg',
    'bracelet': '/gemstone-collection.jpg',
    
    // Default
    'default': '/luxury-jewellery-editorial-hero.jpg'
  }
  
  // Try type first, then category, then default
  return imageMap[type.toLowerCase()] || 
         imageMap[category.toLowerCase()] || 
         imageMap['default']
}

function getProductDescription(product: JewelryItem): string {
  const metal = formatProductName(product.metal)
  const stone = formatProductName(product.stone)
  const type = formatProductName(product.type)
  const brand = formatProductName(product.brand)
  
  const descriptions = [
    `Exquisite ${type} crafted in premium ${metal}, featuring stunning ${stone} in a sophisticated setting. This piece embodies timeless elegance.`,
    `Handcrafted ${type} in lustrous ${metal} with brilliant ${stone} accents. A perfect fusion of artistry and luxury.`,
    `Elegant ${type} showcasing exceptional ${stone} set in finest ${metal}. Designed for those who appreciate refined beauty.`,
    `Stunning ${type} from our ${brand} collection, crafted in ${metal} with exquisite ${stone} details.`
  ]
  
  // Use product ID for consistent selection
  const index = parseInt(product.id.replace(/\D/g, '')) % descriptions.length
  return descriptions[index]
}

// Read the Kaggle jewelry dataset
function getKaggleJewelryDataset(): JewelryItem[] {
  try {
    const jewelryPath = path.join(process.cwd(), 'ml-chatbot', 'models', 'jewelry_dataset.csv')
    
    if (!fs.existsSync(jewelryPath)) {
      console.error('Jewelry dataset not found:', jewelryPath)
      return []
    }
    
    const csvData = fs.readFileSync(jewelryPath, 'utf-8')
    const lines = csvData.split('\n').filter(line => line.trim())
    
    if (lines.length < 2) {
      console.error('Invalid CSV data')
      return []
    }
    
    const headers = lines[0].split(',')
    
    const jewelry = lines.slice(1).map((line, index) => {
      const values = line.split(',')
      if (values.length === headers.length) {
        return {
          id: `kaggle_${index + 1}`,
          category: values[0]?.replace(/"/g, '').trim(),
          type: values[1]?.replace(/"/g, '').trim(),
          metal: values[2]?.replace(/"/g, '').trim(),
          stone: values[3]?.replace(/"/g, '').trim(),
          weight: parseFloat(values[4]) || 0,
          size: parseFloat(values[5]) || 0,
          brand: values[6]?.replace(/"/g, '').trim(),
          price: parseFloat(values[7]) || 0
        }
      }
      return null
    }).filter((item): item is JewelryItem => item !== null)
    
    console.log(`Loaded ${jewelry.length} jewelry items from Kaggle dataset`)
    return jewelry
  } catch (error) {
    console.error('Error loading Kaggle jewelry dataset:', error)
    return []
  }
}

// Simple collection mapping based on actual Kaggle categories
const collectionMapping = {
  'rings': 'ring',
  'necklaces': 'necklace',
  'earrings': 'earrings', 
  'bracelets': 'bracelet'
}

// Collection display information
const collectionsDisplayData = {
  'rings': {
    name: "Rings",
    description: "From statement pieces to elegant wedding bands, discover our collection of expertly crafted rings.",
    heroImage: "/diamond-ring-macro-editorial.jpg"
  },
  'necklaces': {
    name: "Necklaces",
    description: "Elegant chains, pendants, and statement necklaces to complement any style.",
    heroImage: "/gold-necklace-minimal-editorial.jpg"
  },
  'earrings': {
    name: "Earrings", 
    description: "From delicate studs to dramatic chandeliers, find the perfect pair for any occasion.",
    heroImage: "/editorial-jewellery-gallery.jpg"
  },
  'bracelets': {
    name: "Bracelets",
    description: "Sophisticated bangles, tennis bracelets, and charm bracelets for the modern woman.",
    heroImage: "/gemstone-collection.jpg"
  }
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
      title: "Collection | Ornament Tech",
      description: "Discover our curated jewelry collection"
    }
  }

  return {
    title: `${displayData.name} | Ornament Tech`,
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

  // Get distinct products from Kaggle dataset
  const allJewelry = getKaggleJewelryDataset()
  
  // Filter products by category and ensure uniqueness
  const categoryProducts = allJewelry
    .filter(item => item.category === collectionKey)
    .filter((item, index, self) => {
      // Remove duplicates based on type, metal, stone combination
      return index === self.findIndex(p => 
        p.type === item.type && 
        p.metal === item.metal && 
        p.stone === item.stone
      )
    })
    .sort((a, b) => b.price - a.price) // Sort by price descending
    .slice(0, 12) // Limit to 12 unique items

  // Calculate metadata from actual data
  const metadata = categoryProducts.length > 0 ? {
    total_products: categoryProducts.length,
    price_range: `$${Math.min(...categoryProducts.map(p => p.price)).toLocaleString()} - $${Math.max(...categoryProducts.map(p => p.price)).toLocaleString()}`,
    types: [...new Set(categoryProducts.map(p => p.type))].slice(0, 3)
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
          <h1 className="font-serif text-5xl md:text-7xl leading-tight text-pretty mb-6">
            {displayData.name}
          </h1>
          <p className="mt-3 max-w-3xl text-xl md:text-2xl leading-relaxed opacity-90">
            {displayData.description}
          </p>
          {metadata && (
            <div className="mt-6 flex items-center gap-6 text-lg">
              <span className="font-medium">{metadata.total_products} unique pieces</span>
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
                ? `Discover ${categoryProducts.length} distinct pieces from our Kaggle-trained collection` 
                : "Our curated selection of fine jewelry pieces"
              }
            </p>
          </div>

          {categoryProducts.length > 0 ? (
            <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
              {categoryProducts.map((product) => (
                <article 
                  key={product.id} 
                  className="group rounded-2xl overflow-hidden bg-card shadow-lg hover:shadow-2xl transition-all duration-500 hover:-translate-y-2"
                >
                  <div className="relative overflow-hidden">
                    <img
                      src={getProductImage(product.category, product.type)}
                      alt={`${formatProductName(product.type)} ${formatProductName(product.category)}`}
                      className="h-80 w-full object-cover transition-transform duration-700 group-hover:scale-110"
                      onError={(e) => {
                        const target = e.target as HTMLImageElement
                        target.src = '/luxury-jewellery-editorial-hero.jpg'
                      }}
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
    </div>
  )
}