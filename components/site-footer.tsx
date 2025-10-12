import Link from "next/link"

export default function SiteFooter() {
  return (
    <footer className="border-t border-border bg-card">
      <div className="mx-auto max-w-6xl px-4 py-10 grid gap-8 md:grid-cols-4 text-sm">
        <div>
          <h3 className="font-semibold mb-2">Ornament Tech</h3>
          <p className="opacity-70">
            Bespoke jewellery with editorial presentation and an AI concierge to guide your journey.
          </p>
        </div>
        <div>
          <h4 className="font-medium mb-2">Explore</h4>
          <ul className="space-y-1 opacity-90">
            <li>
              <Link href="/bespoke-process">Bespoke Process</Link>
            </li>
            <li>
              <Link href="/collections">Collections</Link>
            </li>
            <li>
              <Link href="/galleries">Galleries</Link>
            </li>
            <li>
              <Link href="/journal">Journal</Link>
            </li>
          </ul>
        </div>
        <div>
          <h4 className="font-medium mb-2">Guides</h4>
          <ul className="space-y-1 opacity-90">
            <li>
              <Link href="/materials">Materials</Link>
            </li>
            <li>
              <Link href="/gemstones">Gemstones</Link>
            </li>
            <li>
              <Link href="/sizing">Sizing</Link>
            </li>
            <li>
              <Link href="/care">Care</Link>
            </li>
          </ul>
        </div>
        <div>
          <h4 className="font-medium mb-2">Company</h4>
          <ul className="space-y-1 opacity-90">
            <li>
              <Link href="/about">About</Link>
            </li>
            <li>
              <Link href="/appointments">Appointments</Link>
            </li>
            <li>
              <Link href="/stores">Stores</Link>
            </li>
            <li>
              <Link href="/contact">Contact</Link>
            </li>
          </ul>
        </div>
      </div>
      <div className="border-t border-border">
        <div className="mx-auto max-w-6xl px-4 py-4 text-xs opacity-70 flex items-center justify-between">
          <span>© {new Date().getFullYear()} Ornament Tech</span>
          <span>
            <Link href="/faq">FAQ</Link>
          </span>
        </div>
      </div>
    </footer>
  )
}
