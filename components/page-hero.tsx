type PageHeroProps = {
  title: string
  subtitle?: string
  imageSrc?: string
  imageAlt?: string
}

export default function PageHero({
  title,
  subtitle,
  imageSrc = "/luxury-jewellery-editorial-hero.jpg",
  imageAlt = "Editorial jewellery hero image",
}: PageHeroProps) {
  return (
    <section className="relative isolate">
      <div className="absolute inset-0 -z-10">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={imageSrc || "/placeholder.svg"}
          alt={imageAlt}
          className="h-64 w-full object-cover object-center md:h-80 lg:h-96"
        />
        <div className="absolute inset-0 bg-background/30" />
      </div>
      <div className="mx-auto max-w-6xl px-4 py-10 md:py-14 lg:py-16">
        <h1 className="font-serif text-3xl md:text-4xl lg:text-5xl text-balance">{title}</h1>
        {subtitle ? <p className="mt-2 max-w-2xl text-muted-foreground leading-relaxed">{subtitle}</p> : null}
      </div>
    </section>
  )
}
