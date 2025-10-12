export const metadata = { title: "Contact — Ornament Tech" }

export default function ContactPage() {
  return (
    <section className="mx-auto max-w-3xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Contact</h1>
      <p className="mt-3 opacity-80">We’d love to hear from you.</p>
      <form className="mt-6 grid gap-4">
        <input className="rounded-md border border-border bg-background px-3 py-2 text-sm" placeholder="Full name" />
        <input className="rounded-md border border-border bg-background px-3 py-2 text-sm" placeholder="Email" />
        <textarea
          className="rounded-md border border-border bg-background px-3 py-2 text-sm"
          placeholder="Message"
          rows={5}
        />
        <button className="rounded-md bg-primary text-primary-foreground px-4 py-2 text-sm w-fit">Send</button>
      </form>
    </section>
  )
}
