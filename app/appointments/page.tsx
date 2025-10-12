export const metadata = { title: "Appointments — Ornament Tech" }

export default function AppointmentsPage() {
  return (
    <section className="mx-auto max-w-3xl px-6 py-12">
      <h1 className="text-3xl font-semibold text-pretty">Book a Consultation</h1>
      <p className="mt-3 opacity-80">Schedule an in-person or virtual appointment to start your bespoke journey.</p>
      <form className="mt-6 grid gap-4">
        <input className="rounded-md border border-border bg-background px-3 py-2 text-sm" placeholder="Full name" />
        <input className="rounded-md border border-border bg-background px-3 py-2 text-sm" placeholder="Email" />
        <input className="rounded-md border border-border bg-background px-3 py-2 text-sm" placeholder="Phone" />
        <textarea
          className="rounded-md border border-border bg-background px-3 py-2 text-sm"
          placeholder="Project details"
          rows={5}
        />
        <button className="rounded-md bg-primary text-primary-foreground px-4 py-2 text-sm w-fit">
          Request Booking
        </button>
      </form>
      <p className="mt-3 text-sm opacity-70">For quick questions, try the chat in the corner.</p>
    </section>
  )
}
