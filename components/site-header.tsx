"use client"

import Link from "next/link"
import { useState } from "react"
import { usePathname } from "next/navigation"

export default function SiteHeader() {
  const [open, setOpen] = useState(false)
  const pathname = usePathname()
  const links = [
    { href: "/bespoke-process", label: "Bespoke" },
    { href: "/collections", label: "Collections" },
    { href: "/galleries", label: "Galleries" },
    { href: "/materials", label: "Materials" },
    { href: "/gemstones", label: "Gemstones" },
    { href: "/sizing", label: "Sizing" },
    { href: "/appointments", label: "Appointments" },
    { href: "/journal", label: "Journal" },
    { href: "/about", label: "About" },
    { href: "/contact", label: "Contact" },
  ]
  return (
    <header className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto max-w-6xl px-4 py-3 flex items-center justify-between">
        <Link href="/" className="text-xl font-serif tracking-wide">
          Ornament Tech
          <span className="sr-only">Home</span>
        </Link>
        <nav className="hidden md:flex items-center gap-5 text-sm">
          {links.map((l) => {
            const isActive = pathname === l.href || (l.href !== "/" && pathname?.startsWith(l.href))
            return (
              <Link
                key={l.href}
                href={l.href}
                aria-current={isActive ? "page" : undefined}
                className={
                  isActive
                    ? "text-foreground font-medium underline underline-offset-4 decoration-2"
                    : "text-muted-foreground hover:text-foreground transition-colors"
                }
              >
                {l.label}
              </Link>
            )
          })}
          <a
            href="https://wa.me/1234567890"
            target="_blank"
            rel="noopener noreferrer"
            className="ml-2 inline-flex items-center gap-1 rounded-md bg-green-600 text-white px-3 py-1.5 text-xs hover:bg-green-700 transition-colors"
          >
            <span>💬</span>
            WhatsApp
          </a>
        </nav>
        <button
          className="md:hidden inline-flex items-center gap-2 rounded-md px-3 py-2 text-sm border hover:bg-muted/40 transition-colors"
          onClick={() => setOpen(!open)}
          aria-expanded={open}
          aria-controls="mobile-menu"
          aria-label="Toggle navigation menu"
        >
          Menu
        </button>
      </div>
      {open && (
        <nav id="mobile-menu" className="md:hidden border-t bg-background/95 backdrop-blur">
          <div className="mx-auto max-w-6xl px-4 py-3 grid grid-cols-2 gap-3 text-sm">
            {links.map((l) => {
              const isActive = pathname === l.href || (l.href !== "/" && pathname?.startsWith(l.href))
              return (
                <Link
                  key={l.href}
                  href={l.href}
                  aria-current={isActive ? "page" : undefined}
                  className={
                    isActive
                      ? "text-foreground font-medium underline underline-offset-4 decoration-2"
                      : "text-muted-foreground hover:text-foreground transition-colors"
                  }
                >
                  {l.label}
                </Link>
              )
            })}
          </div>
        </nav>
      )}
    </header>
  )
}
