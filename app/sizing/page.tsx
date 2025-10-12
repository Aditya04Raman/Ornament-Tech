export const metadata = { title: "Sizing — Ornament Tech" }

export default function SizingPage() {
  return (
    <section className="mx-auto max-w-4xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Sizing Guide</h1>
      <p className="mt-3 opacity-80">
        Tips for accurate ring sizing, international conversions, and comfort-fit recommendations.
      </p>
      <div className="mt-6 rounded-lg border border-border bg-card p-5">
        <ul className="list-disc pl-5 space-y-2 text-sm opacity-90">
          <li>Measure at the end of the day when fingers are warm.</li>
          <li>Consider width: wider bands feel tighter.</li>
          <li>Consult our team for printable sizing tools and advice.</li>
        </ul>
      </div>
    </section>
  )
}
