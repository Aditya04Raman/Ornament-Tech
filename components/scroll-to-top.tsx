"use client"

import { useState, useEffect } from "react"
import Link from "next/link"

export default function ScrollToTop() {
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const toggleVisibility = () => {
      if (window.pageYOffset > 300) {
        setIsVisible(true)
      } else {
        setIsVisible(false)
      }
    }

    window.addEventListener("scroll", toggleVisibility)
    return () => window.removeEventListener("scroll", toggleVisibility)
  }, [])

  const scrollToTop = () => {
    window.scrollTo({
      top: 0,
      behavior: "smooth"
    })
  }

  return (
    <>
      {/* Scroll to Top Button */}
      {isVisible && (
        <button
          onClick={scrollToTop}
          className="fixed bottom-24 left-6 z-40 rounded-full bg-primary text-primary-foreground p-3 shadow-lg hover:bg-primary/90 transition-all duration-300"
          aria-label="Scroll to top"
        >
          ↑
        </button>
      )}
      
      {/* Home Button */}
      <Link
        href="/"
        className="fixed bottom-6 left-6 z-40 rounded-full bg-accent text-accent-foreground px-4 py-3 shadow-lg hover:bg-accent/90 transition-all duration-300 text-sm font-medium"
      >
        🏠 Home
      </Link>
    </>
  )
}
