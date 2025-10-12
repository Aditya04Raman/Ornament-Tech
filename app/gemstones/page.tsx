export const metadata = { title: "Gemstones — Ornament Tech" }

export default function GemstonesPage() {
  const stones = [
    { title: "Diamonds", body: "Understand the 4Cs: cut, color, clarity, carat." },
    { title: "Sapphire", body: "Durable corundum in a range of colors." },
    { title: "Emerald", body: "Vibrant green beryl with unique inclusions." },
    { title: "Ruby", body: "Rich red corundum prized for its intensity." },
  ]
  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Gemstones</h1>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        {stones.map((s) => (
          <div key={s.title} className="rounded-lg border border-border bg-card p-5">
            <h3 className="font-medium">{s.title}</h3>
            <p className="mt-2 text-sm opacity-80">{s.body}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
