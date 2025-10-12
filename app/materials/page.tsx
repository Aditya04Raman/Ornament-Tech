export const metadata = { title: "Materials — Ornament Tech" }

export default function MaterialsPage() {
  const materials = [
    { title: "Platinum", body: "Durable, naturally white, hypoallergenic." },
    { title: "18K Yellow Gold", body: "Warm hue with excellent wear properties." },
    { title: "18K White Gold", body: "Bright, rhodium-finished; periodic maintenance recommended." },
    { title: "18K Rose Gold", body: "Copper alloy for a romantic blush tone." },
  ]
  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Materials</h1>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        {materials.map((m) => (
          <div key={m.title} className="rounded-lg border border-border bg-card p-5">
            <h3 className="font-medium">{m.title}</h3>
            <p className="mt-2 text-sm opacity-80">{m.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
