// Recommended: Use Next.js Image component for better performance
// Example for app/page.tsx

import Image from 'next/image'

// Replace:
<img src="/diamond-ring-on-velvet-close-up-luxury-editorial.jpg" alt="..." />

// With:
<Image
  src="/diamond-ring-on-velvet-close-up-luxury-editorial.jpg"
  alt="Diamond engagement ring on velvet"
  width={1200}
  height={800}
  className="h-[60vh] md:h-[72vh] w-full object-cover"
  priority // for above-the-fold images
/>
