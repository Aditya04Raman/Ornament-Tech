export const metadata = { title: "Galleries — Ornament Tech" }

export default function GalleriesPage() {
  const categories = ["Rings", "Bands", "Necklaces", "Earrings", "Bracelets", "Custom Sets"]
  return (
    <section className="mx-auto max-w-6xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Galleries</h1>
      <p className="mt-3 opacity-80">Editorial showcases across categories.</p>
      <div className="mt-6 grid gap-5 md:grid-cols-3">
        {categories.map((cat) => (
          <div key={cat} className="rounded-lg border border-border bg-card p-4">
            <div className="aspect-[4/3] rounded-md border border-border bg-muted" aria-hidden />
            <h3 className="mt-3 font-medium">{cat}</h3>
          </div>
        ))}
      </div>
    </section>
  )
}
