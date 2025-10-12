import Link from "next/link"

export const metadata = { title: "Journal — Ornament Tech" }

export default function JournalPage() {
  const posts = [
    { slug: "choosing-your-diamond", title: "Choosing Your Diamond", excerpt: "A clear guide to the 4Cs." },
    { slug: "behind-the-craft", title: "Behind the Craft", excerpt: "How our atelier brings designs to life." },
  ]
  return (
    <section className="mx-auto max-w-5xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Journal</h1>
      <div className="mt-6 grid gap-6 md:grid-cols-2">
        {posts.map((p) => (
          <article key={p.slug} className="rounded-lg border border-border bg-card p-5">
            <h3 className="font-medium">
              <Link href={`/journal/${p.slug}`}>{p.title}</Link>
            </h3>
            <p className="mt-2 text-sm opacity-80">{p.excerpt}</p>
          </article>
        ))}
      </div>
    </section>
  )
}
