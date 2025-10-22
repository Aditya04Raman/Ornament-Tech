"use client"

import { useState } from "react"
import Image from "next/image"
import Link from "next/link"

export default function SizingPage() {
  const [selectedSize, setSelectedSize] = useState<number | null>(null)
  const [ringWidth, setRingWidth] = useState<string>("standard")

  const ringSizes = [
    { us: 3, uk: "F", eu: 44, mm: 14.1 },
    { us: 4, uk: "H", eu: 47, mm: 14.9 },
    { us: 5, uk: "J", eu: 49, mm: 15.7 },
    { us: 6, uk: "L", eu: 52, mm: 16.5 },
    { us: 7, uk: "N", eu: 54, mm: 17.3 },
    { us: 8, uk: "P", eu: 57, mm: 18.1 },
    { us: 9, uk: "R", eu: 59, mm: 19.0 },
    { us: 10, uk: "T", eu: 62, mm: 19.8 },
    { us: 11, uk: "V", eu: 64, mm: 20.6 },
    { us: 12, uk: "X", eu: 67, mm: 21.4 },
  ]

  const sizingTips = [
    {
      icon: "🕐",
      title: "Best Time to Measure",
      tip: "Measure at the end of the day when fingers are naturally warmer and slightly larger."
    },
    {
      icon: "🌡️",
      title: "Temperature Matters",
      tip: "Avoid measuring when hands are cold or immediately after exercise when they may be swollen."
    },
    {
      icon: "📏",
      title: "Width Considerations",
      tip: "Wider bands (6mm+) feel tighter than thin bands. Consider sizing up 0.5 sizes for comfort."
    },
    {
      icon: "💍",
      title: "Comfort Fit",
      tip: "Comfort fit rings have a rounded interior and typically require 0.5 size smaller than standard fit."
    }
  ]

  const widthAdjustments = {
    thin: { label: "Thin (1-3mm)", adjustment: 0 },
    standard: { label: "Standard (3-6mm)", adjustment: 0 },
    wide: { label: "Wide (6-8mm)", adjustment: 0.5 },
    extraWide: { label: "Extra Wide (8mm+)", adjustment: 1 }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Hero Section */}
      <section className="relative py-16 bg-gradient-to-r from-primary to-accent text-white">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative mx-auto max-w-6xl px-6 text-center">
          <h1 className="text-4xl md:text-5xl font-serif font-bold mb-4">
            Perfect Fit Guarantee
          </h1>
          <p className="text-xl md:text-2xl text-white/90 max-w-3xl mx-auto leading-relaxed">
            Find your ideal ring size with our comprehensive sizing guide, tools, and expert consultation.
          </p>
        </div>
      </section>

      {/* Interactive Size Calculator */}
      <section id="ring-sizer" className="mx-auto max-w-6xl px-6 py-16">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-serif font-semibold mb-4">Interactive Ring Sizer</h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Use our digital sizing tool to find your perfect fit, with adjustments for different ring widths.
          </p>
        </div>

        <div className="grid gap-12 lg:grid-cols-2">
          {/* Size Selection */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h3 className="text-xl font-semibold mb-6">Select Your Ring Width</h3>
            
            <div className="grid grid-cols-2 gap-3 mb-8">
              {Object.entries(widthAdjustments).map(([key, width]) => (
                <button
                  key={key}
                  onClick={() => setRingWidth(key)}
                  className={`p-4 rounded-lg text-left transition-all duration-200 ${
                    ringWidth === key
                      ? 'bg-gradient-to-r from-primary to-accent text-white shadow-lg'
                      : 'bg-gray-50 hover:bg-gray-100 text-gray-700'
                  }`}
                >
                  <div className="font-medium">{width.label}</div>
                  {width.adjustment > 0 && (
                    <div className="text-sm opacity-80">+{width.adjustment} size adjustment</div>
                  )}
                </button>
              ))}
            </div>

            <h3 className="text-xl font-semibold mb-6">Your Measurements</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ring Circumference (mm)
                </label>
                <input
                  type="number"
                  placeholder="Enter circumference in mm"
                  className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  onChange={(e) => {
                    const circumference = parseFloat(e.target.value)
                    if (circumference) {
                      const diameter = circumference / Math.PI
                      const closestSize = ringSizes.reduce((prev, curr) => 
                        Math.abs(curr.mm - diameter) < Math.abs(prev.mm - diameter) ? curr : prev
                      )
                      setSelectedSize(closestSize.us)
                    }
                  }}
                />
              </div>
              <div className="text-center text-gray-600">or</div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Ring Diameter (mm)
                </label>
                <input
                  type="number"
                  placeholder="Enter diameter in mm"
                  className="w-full px-4 py-3 border border-gray-200 rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
                  onChange={(e) => {
                    const diameter = parseFloat(e.target.value)
                    if (diameter) {
                      const closestSize = ringSizes.reduce((prev, curr) => 
                        Math.abs(curr.mm - diameter) < Math.abs(prev.mm - diameter) ? curr : prev
                      )
                      setSelectedSize(closestSize.us)
                    }
                  }}
                />
              </div>
            </div>
          </div>

          {/* Size Chart */}
          <div className="bg-white rounded-2xl shadow-lg p-8">
            <h3 className="text-xl font-semibold mb-6">Size Conversion Chart</h3>
            
            <div className="overflow-hidden rounded-lg border border-gray-200">
              <div className="grid grid-cols-4 bg-gray-50 p-3 text-sm font-medium text-gray-700">
                <div>US</div>
                <div>UK</div>
                <div>EU</div>
                <div>Diameter (mm)</div>
              </div>
              
              {ringSizes.map((size) => {
                const adjustedSize = size.us + (widthAdjustments[ringWidth as keyof typeof widthAdjustments]?.adjustment || 0)
                const isSelected = selectedSize === size.us
                
                return (
                  <div
                    key={size.us}
                    className={`grid grid-cols-4 p-3 text-sm border-t border-gray-100 cursor-pointer transition-colors ${
                      isSelected 
                        ? 'bg-gradient-to-r from-primary/10 to-accent/10 border-primary/20' 
                        : 'hover:bg-gray-50'
                    }`}
                    onClick={() => setSelectedSize(size.us)}
                  >
                    <div className="font-medium">{adjustedSize}</div>
                    <div>{size.uk}</div>
                    <div>{size.eu}</div>
                    <div>{size.mm}</div>
                  </div>
                )
              })}
            </div>

            {selectedSize && (
              <div className="mt-6 p-4 bg-gradient-to-r from-primary/10 to-accent/10 rounded-lg">
                <h4 className="font-semibold text-primary mb-2">Recommended Size</h4>
                <p className="text-sm">
                  Based on your measurements and selected width ({widthAdjustments[ringWidth as keyof typeof widthAdjustments]?.label}), 
                  we recommend a US size {selectedSize + (widthAdjustments[ringWidth as keyof typeof widthAdjustments]?.adjustment || 0)}.
                </p>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Sizing Tips */}
      <section className="bg-gray-50 py-16">
        <div className="mx-auto max-w-6xl px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-serif font-semibold mb-4">Professional Sizing Tips</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Expert advice to ensure your ring fits perfectly and comfortably.
            </p>
          </div>

          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
            {sizingTips.map((tip, index) => (
              <div key={index} className="bg-white rounded-xl p-6 shadow-sm hover:shadow-lg transition-shadow duration-300">
                <div className="text-3xl mb-4">{tip.icon}</div>
                <h3 className="font-semibold text-lg mb-3">{tip.title}</h3>
                <p className="text-sm text-gray-600 leading-relaxed">{tip.tip}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* International Sizing */}
      <section id="international" className="py-16">
        <div className="mx-auto max-w-4xl px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-serif font-semibold mb-4">International Size Standards</h2>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Understanding different sizing systems worldwide for accurate conversion.
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-3">
            <div className="bg-white rounded-xl p-6 shadow-sm text-center">
              <h3 className="font-semibold text-lg mb-3">US Sizing</h3>
              <p className="text-sm text-gray-600 mb-4">
                Numerical system from 3-13, most common in North America.
              </p>
              <div className="text-2xl font-bold text-primary">3 - 13</div>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-sm text-center">
              <h3 className="font-semibold text-lg mb-3">UK Sizing</h3>
              <p className="text-sm text-gray-600 mb-4">
                Alphabetical system from A-Z, traditional British standard.
              </p>
              <div className="text-2xl font-bold text-primary">A - Z</div>
            </div>

            <div className="bg-white rounded-xl p-6 shadow-sm text-center">
              <h3 className="font-semibold text-lg mb-3">EU Sizing</h3>
              <p className="text-sm text-gray-600 mb-4">
                Circumference-based system, used across European markets.
              </p>
              <div className="text-2xl font-bold text-primary">44 - 67</div>
            </div>
          </div>
        </div>
      </section>

      {/* Comfort Fit Guide */}
      <section id="comfort-fit" className="bg-gradient-to-r from-gray-100 to-gray-50 py-16">
        <div className="mx-auto max-w-6xl px-6">
          <div className="grid gap-12 lg:grid-cols-2 items-center">
            <div>
              <h2 className="text-3xl font-serif font-semibold mb-6">Comfort Fit vs Standard Fit</h2>
              
              <div className="space-y-6">
                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <h3 className="font-semibold text-lg mb-3 text-primary">Standard Fit</h3>
                  <p className="text-gray-600 mb-3">
                    Flat interior surface with sharp edges. Traditional design that sits flush against the finger.
                  </p>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• More metal contact with finger</li>
                    <li>• Traditional jewelry standard</li>
                    <li>• True to marked size</li>
                  </ul>
                </div>

                <div className="bg-white rounded-lg p-6 shadow-sm">
                  <h3 className="font-semibold text-lg mb-3 text-accent">Comfort Fit</h3>
                  <p className="text-gray-600 mb-3">
                    Rounded interior surface that's domed for easier wearing and removal.
                  </p>
                  <ul className="text-sm text-gray-600 space-y-1">
                    <li>• Slides on and off easily</li>
                    <li>• Less metal contact with skin</li>
                    <li>• Size down 0.5 sizes typically needed</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="relative">
              <div className="bg-white rounded-2xl p-8 shadow-lg">
                <Image
                  src="/ring-sizing-guide-editorial.jpg"
                  alt="Ring sizing guide"
                  width={400}
                  height={300}
                  className="w-full rounded-lg"
                />
                <div className="mt-6 text-center">
                  <p className="text-sm text-gray-600 mb-4">
                    Professional sizing consultation available
                  </p>
                  <Link 
                    href="/appointments"
                    className="bg-gradient-to-r from-primary to-accent text-white py-3 px-6 rounded-lg font-medium hover:shadow-lg transform hover:scale-105 transition-all duration-200"
                  >
                    Book Sizing Appointment
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-16">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <h2 className="text-3xl font-serif font-semibold mb-4">Still Unsure About Your Size?</h2>
          <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
            Our sizing specialists are here to help. We offer complimentary sizing consultations 
            and can send you a professional ring sizer for the most accurate measurement.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link 
              href="/contact"
              className="bg-gradient-to-r from-primary to-accent text-white py-3 px-8 rounded-lg font-medium hover:shadow-lg transform hover:scale-105 transition-all duration-200"
            >
              Request Ring Sizer
            </Link>
            <Link 
              href="/appointments"
              className="border border-gray-300 text-gray-700 py-3 px-8 rounded-lg font-medium hover:bg-gray-50 transition-colors duration-200"
            >
              Schedule Consultation
            </Link>
          </div>
        </div>
      </section>
    </div>
  )
}
