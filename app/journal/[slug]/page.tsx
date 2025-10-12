interface Params {
  slug: string
}

export default function JournalPostPage({ params }: { params: Params }) {
  return (
    <section className="mx-auto max-w-3xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">{params.slug.replace(/-/g, " ")}</h1>
      <p className="mt-3 opacity-80">This is a placeholder article. Replace with your long-form content and imagery.</p>
      <div className="mt-6 rounded-lg border border-border bg-card p-5 text-sm leading-relaxed opacity-90">
        <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque habitant morbi tristique senectus.</p>
      </div>
    </section>
  )
}
