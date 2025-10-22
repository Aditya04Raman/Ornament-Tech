import Link from "next/link"
import Image from "next/image"

export const metadata = { title: "Journal — Ornament Tech" }

export default function JournalPage() {
  const featuredPost = {
    slug: "choosing-your-diamond",
    title: "The Complete Guide to Choosing Your Perfect Diamond",
    excerpt: "Navigate the world of diamonds with confidence. Our comprehensive guide covers the 4Cs, certification, and finding exceptional value in your diamond selection.",
    image: "/diamond-ring-macro-editorial.jpg",
    author: "Sarah Mitchell",
    date: "October 15, 2025",
    readTime: "8 min read",
    category: "Education"
  }

  const posts = [
    { 
      slug: "behind-the-craft", 
      title: "Behind the Craft: Our Artisan's Journey", 
      excerpt: "Step inside our atelier and discover how master craftsmen bring bespoke jewelry designs to life through traditional techniques and modern innovation.",
      image: "/artisan-craftsmanship-jewellery.jpg",
      author: "Marcus Chen",
      date: "October 12, 2025",
      readTime: "6 min read",
      category: "Craftsmanship"
    },
    {
      slug: "gemstone-sourcing",
      title: "Ethical Gemstone Sourcing: Our Commitment",
      excerpt: "Learn about our responsible sourcing practices and the journey of gemstones from mine to masterpiece.",
      image: "/gemstone-collection.jpg",
      author: "Emma Thompson",
      date: "October 10, 2025",
      readTime: "5 min read",
      category: "Sustainability"
    },
    {
      slug: "vintage-revival",
      title: "Vintage Revival: Timeless Design Elements",
      excerpt: "Explore how vintage jewelry influences contemporary design and why certain styles remain eternally elegant.",
      image: "/heritage-jewellery-collection.jpg",
      author: "David Rousseau",
      date: "October 8, 2025",
      readTime: "7 min read",
      category: "Design"
    },
    {
      slug: "jewelry-care-guide",
      title: "Caring for Your Precious Pieces",
      excerpt: "Expert tips for maintaining the brilliance and longevity of your fine jewelry collection.",
      image: "/jewellery-care-kit.jpg",
      author: "Lisa Park",
      date: "October 5, 2025",
      readTime: "4 min read",
      category: "Care"
    }
  ]

  const categories = [
    { name: "All", count: 12, active: true },
    { name: "Education", count: 4, active: false },
    { name: "Craftsmanship", count: 3, active: false },
    { name: "Design", count: 3, active: false },
    { name: "Sustainability", count: 2, active: false },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <section className="relative py-16 bg-gradient-to-r from-primary to-accent text-white">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative mx-auto max-w-6xl px-6 text-center">
          <h1 className="text-4xl md:text-5xl font-serif font-bold mb-4">
            Jewelry Journal
          </h1>
          <p className="text-xl md:text-2xl text-white/90 max-w-3xl mx-auto leading-relaxed">
            Insights, stories, and expertise from the world of fine jewelry. 
            Discover the artistry, history, and craftsmanship behind exceptional pieces.
          </p>
        </div>
      </section>

      <div className="mx-auto max-w-6xl px-6 py-16">
        {/* Featured Article */}
        <section className="mb-16">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-serif font-semibold mb-4">Featured Article</h2>
            <p className="text-lg text-gray-600">Our latest insights and expertise</p>
          </div>

          <article className="bg-white rounded-2xl shadow-xl overflow-hidden hover:shadow-2xl transition-shadow duration-500">
            <div className="grid lg:grid-cols-2">
              <div className="relative h-64 lg:h-full">
                <Image
                  src={featuredPost.image}
                  alt={featuredPost.title}
                  fill
                  className="object-cover"
                />
                <div className="absolute top-4 left-4">
                  <span className="bg-primary text-white px-3 py-1 rounded-full text-sm font-medium">
                    {featuredPost.category}
                  </span>
                </div>
              </div>
              
              <div className="p-8 lg:p-12 flex flex-col justify-center">
                <div className="flex items-center gap-4 text-sm text-gray-500 mb-4">
                  <span>{featuredPost.author}</span>
                  <span>•</span>
                  <span>{featuredPost.date}</span>
                  <span>•</span>
                  <span>{featuredPost.readTime}</span>
                </div>
                
                <h3 className="text-2xl lg:text-3xl font-serif font-bold mb-4 leading-tight">
                  <Link href={`/journal/${featuredPost.slug}`} className="hover:text-primary transition-colors">
                    {featuredPost.title}
                  </Link>
                </h3>
                
                <p className="text-gray-600 mb-6 leading-relaxed">
                  {featuredPost.excerpt}
                </p>
                
                <Link 
                  href={`/journal/${featuredPost.slug}`}
                  className="inline-flex items-center gap-2 bg-gradient-to-r from-primary to-accent text-white py-3 px-6 rounded-lg font-medium hover:shadow-lg transform hover:scale-105 transition-all duration-200 w-fit"
                >
                  Read Full Article
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                  </svg>
                </Link>
              </div>
            </div>
          </article>
        </section>

        {/* Categories */}
        <section className="mb-12">
          <div className="flex flex-wrap justify-center gap-3">
            {categories.map((category) => (
              <button
                key={category.name}
                className={`px-6 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                  category.active
                    ? 'bg-gradient-to-r from-primary to-accent text-white shadow-lg'
                    : 'bg-white text-gray-600 border border-gray-200 hover:border-primary hover:text-primary'
                }`}
              >
                {category.name} ({category.count})
              </button>
            ))}
          </div>
        </section>

        {/* Articles Grid */}
        <section>
          <div className="grid gap-8 md:grid-cols-2">
            {posts.map((post) => (
              <article key={post.slug} className="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300">
                <div className="relative h-48 overflow-hidden">
                  <Image
                    src={post.image}
                    alt={post.title}
                    fill
                    className="object-cover group-hover:scale-110 transition-transform duration-500"
                  />
                  <div className="absolute top-4 left-4">
                    <span className="bg-white/90 backdrop-blur-sm text-gray-800 px-3 py-1 rounded-full text-sm font-medium">
                      {post.category}
                    </span>
                  </div>
                </div>
                
                <div className="p-6">
                  <div className="flex items-center gap-3 text-xs text-gray-500 mb-3">
                    <span>{post.author}</span>
                    <span>•</span>
                    <span>{post.date}</span>
                    <span>•</span>
                    <span>{post.readTime}</span>
                  </div>
                  
                  <h3 className="text-xl font-serif font-semibold mb-3 leading-tight">
                    <Link href={`/journal/${post.slug}`} className="hover:text-primary transition-colors">
                      {post.title}
                    </Link>
                  </h3>
                  
                  <p className="text-gray-600 text-sm leading-relaxed mb-4">
                    {post.excerpt}
                  </p>
                  
                  <Link 
                    href={`/journal/${post.slug}`}
                    className="inline-flex items-center gap-2 text-primary font-medium text-sm hover:gap-3 transition-all duration-200"
                  >
                    Read More
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                    </svg>
                  </Link>
                </div>
              </article>
            ))}
          </div>
        </section>

        {/* Load More */}
        <section className="text-center mt-12">
          <Link 
            href="/journal?page=2"
            className="border border-gray-300 text-gray-700 py-3 px-8 rounded-lg font-medium hover:bg-gray-50 transition-colors duration-200 inline-block"
          >
            Load More Articles
          </Link>
        </section>
      </div>

      {/* Newsletter Signup */}
      <section id="care-tips" className="bg-gradient-to-r from-gray-100 to-gray-50 py-16">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="text-3xl font-serif font-semibold mb-4">Stay Informed</h2>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Subscribe to our journal for the latest insights on jewelry care, design trends, 
            and exclusive stories from our atelier.
          </p>
          
          <div className="max-w-md mx-auto">
            <div className="flex gap-3">
              <input
                type="email"
                placeholder="Enter your email"
                className="flex-1 px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
              />
              <Link 
                href="/contact"
                className="bg-gradient-to-r from-primary to-accent text-white py-3 px-6 rounded-lg font-medium hover:shadow-lg transform hover:scale-105 transition-all duration-200"
              >
                Subscribe
              </Link>
            </div>
            <p className="text-xs text-gray-500 mt-3">
              No spam, unsubscribe at any time. Read our privacy policy.
            </p>
          </div>
        </div>
      </section>
    </div>
  )
}
