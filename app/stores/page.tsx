export const metadata = { title: "Stores — Ornament Tech" }

export default function StoresPage() {
  const stores = [
    { city: "London", info: "Flagship studio. Appointments recommended." },
    { city: "Cambridge", info: "Boutique showroom. Walk-ins welcome when available." },
  ]
  return (
    <section className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Stores</h1>
      <div className="mt-6 grid gap-4 md:grid-cols-2">
        {stores.map((s) => (
          <div key={s.city} className="rounded-lg border border-border bg-card p-5">
            <h3 className="font-medium">{s.city}</h3>
            <p className="mt-2 text-sm opacity-80">{s.info}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
