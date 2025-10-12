import type React from "react"
import type { Metadata } from "next"
import { Inter, Cormorant_Garamond } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import { Suspense } from "react"
import SiteHeader from "@/components/site-header"
import SiteFooter from "@/components/site-footer"
import ChatWidget from "@/components/chat-widget"
import "./globals.css"

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" })
const cormorant = Cormorant_Garamond({ subsets: ["latin"], variable: "--font-cormorant" })

export const metadata: Metadata = {
  title: "Ornament Tech",
  description: "Ornament Tech — Bespoke jewellery, editorial presentation, and AI concierge",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={`${inter.variable} ${cormorant.variable} antialiased`}>
      <body className="font-sans">
        <SiteHeader />
        <main>{children}</main>
        <SiteFooter />
        <ChatWidget />
        <Suspense fallback={null}></Suspense>
        <Analytics />
      </body>
    </html>
  )
}
