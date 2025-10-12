export const metadata = { title: "Bespoke Process — Ornament Tech" }

export default function BespokeProcessPage() {
  const steps = [
    { title: "Consultation", body: "Discuss ideas, budget, timelines, and inspirations." },
    { title: "Design", body: "Sketches, CAD, and material selection for your piece." },
    { title: "Craft", body: "Expert goldsmithing and gemstone setting in our atelier." },
    { title: "Delivery", body: "Final quality checks and presentation." },
  ]
  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Bespoke Process</h1>
      <p className="mt-3 opacity-80 leading-relaxed">From concept to creation, a guided journey tailored to you.</p>
      <div className="mt-8 grid gap-4 md:grid-cols-2">
        {steps.map((s) => (
          <div key={s.title} className="rounded-lg border border-border bg-card p-5">
            <h3 className="font-medium">{s.title}</h3>
            <p className="mt-2 text-sm opacity-80">{s.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
