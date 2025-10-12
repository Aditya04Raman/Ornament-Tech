export const metadata = { title: "Care — Ornament Tech" }

export default function CarePage() {
  return (
    <section className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Care & Maintenance</h1>
      <p className="mt-3 opacity-80">Keep your jewellery brilliant with regular cleaning and mindful wear.</p>
      <ul className="mt-4 list-disc pl-5 text-sm opacity-90 space-y-2">
        <li>Remove jewellery during strenuous activities or exposure to chemicals.</li>
        <li>Clean gently with warm water, mild soap, and a soft brush.</li>
        <li>Schedule professional checks for settings and prongs.</li>
      </ul>
    </section>
  )
}
