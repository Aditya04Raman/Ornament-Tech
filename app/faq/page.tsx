export const metadata = { title: "FAQ — Ornament Tech" }

export default function FAQPage() {
  const faqs = [
    { q: "What are typical lead times?", a: "Bespoke projects typically take 4–8 weeks depending on complexity." },
    { q: "Do you resize rings?", a: "Yes, we offer resizing services and guidance via our Sizing page." },
    { q: "What’s a typical budget?", a: "Budgets vary widely; consult with us for tailored recommendations." },
  ]
  return (
    <section className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">FAQ</h1>
      <div className="mt-6 space-y-4">
        {faqs.map((f) => (
          <div key={f.q} className="rounded-lg border border-border bg-card p-5">
            <h3 className="font-medium">{f.q}</h3>
            <p className="mt-2 text-sm opacity-80">{f.a}</p>
          </div>
        ))}
      </div>
    </section>
  )
}
