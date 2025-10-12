export const metadata = { title: "Craftsmanship — Ornament Tech" }

export default function CraftsmanshipPage() {
  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Craftsmanship</h1>
      <p className="mt-3 opacity-80">
        Our atelier combines modern techniques with traditional goldsmithing for enduring quality.
      </p>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        <div className="rounded-lg border border-border bg-card p-5">
          <h3 className="font-medium">Design & Prototyping</h3>
          <p className="mt-2 text-sm opacity-80">From sketch to CAD, every detail is honed before crafting.</p>
        </div>
        <div className="rounded-lg border border-border bg-card p-5">
          <h3 className="font-medium">Setting & Finishing</h3>
          <p className="mt-2 text-sm opacity-80">Precise stone setting and finishing for lasting brilliance.</p>
        </div>
      </div>
    </section>
  )
}
