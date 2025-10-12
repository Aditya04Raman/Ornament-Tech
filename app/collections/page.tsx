export const metadata = { title: "Collections — Ornament Tech" }

export default function CollectionsPage() {
  const collections = [
    { name: "Engagement Rings", desc: "Solitaire, halo, trilogy, and custom designs." },
    { name: "Wedding Bands", desc: "Classic, shaped, textured, and bespoke fits." },
    { name: "Necklaces", desc: "Pendants and statement designs with precious stones." },
    { name: "Earrings", desc: "Studs, hoops, and drops in precious metals." },
  ]
  return (
    <section className="mx-auto max-w-6xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Collections</h1>
      <div className="mt-6 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {collections.map((c) => (
          <article key={c.name} className="rounded-lg border border-border bg-card p-5">
            <div className="aspect-[4/3] rounded-md border border-border bg-muted" aria-hidden />
            <h3 className="mt-3 font-medium">{c.name}</h3>
            <p className="mt-2 text-sm opacity-80">{c.desc}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
