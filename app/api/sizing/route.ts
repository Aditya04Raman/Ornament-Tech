import { NextRequest, NextResponse } from 'next/server'

interface SizingRequest {
  email: string
  name: string
  address: {
    street: string
    city: string
    postalCode: string
    country: string
  }
  ringType: string
  notes?: string
}

export async function POST(request: NextRequest) {
  try {
    const data: SizingRequest = await request.json()

    // Validation
    if (!data.email || !data.name || !data.address) {
      return NextResponse.json(
        { error: 'Email, name, and address are required' },
        { status: 400 }
      )
    }

    // Here you would:
    // 1. Create shipping label
    // 2. Send confirmation email
    // 3. Log request in database

    console.log('Ring sizer request:', data)

    // TODO: Implement shipping integration
    // TODO: Send confirmation email
    // TODO: Store in database

    return NextResponse.json({ 
      success: true, 
      message: 'Ring sizer request received! We will ship it within 2 business days.',
      trackingId: `SIZER-${Date.now()}`
    })

  } catch (error) {
    console.error('Ring sizer request error:', error)
    return NextResponse.json(
      { error: 'Failed to process request. Please try again.' },
      { status: 500 }
    )
  }
}

// GET endpoint for size calculations
export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const circumference = searchParams.get('circumference')
  const diameter = searchParams.get('diameter')
  const width = searchParams.get('width') || 'standard'

  if (!circumference && !diameter) {
    return NextResponse.json(
      { error: 'Either circumference or diameter is required' },
      { status: 400 }
    )
  }

  // Size calculation logic
  let calcDiameter: number
  if (circumference) {
    calcDiameter = parseFloat(circumference) / Math.PI
  } else {
    calcDiameter = parseFloat(diameter!)
  }

  // Size chart mapping (simplified)
  const sizeChart = [
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

  // Find closest size
  const closestSize = sizeChart.reduce((prev, curr) => 
    Math.abs(curr.mm - calcDiameter) < Math.abs(prev.mm - calcDiameter) ? curr : prev
  )

  // Width adjustments
  const widthAdjustments: { [key: string]: number } = {
    thin: 0,
    standard: 0,
    wide: 0.5,
    extraWide: 1
  }

  const adjustment = widthAdjustments[width] || 0
  const recommendedSize = closestSize.us + adjustment

  return NextResponse.json({
    inputDiameter: calcDiameter,
    closestMatch: closestSize,
    widthAdjustment: adjustment,
    recommendedSize,
    recommendation: `Based on your measurements, we recommend US size ${recommendedSize}`
  })
}