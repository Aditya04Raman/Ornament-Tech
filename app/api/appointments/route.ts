import { NextRequest, NextResponse } from 'next/server'

interface AppointmentData {
  firstName: string
  lastName: string
  email: string
  phone?: string
  consultationType: string
  location: string
  projectType: string
  budgetRange: string
  projectDescription: string
  preferredDateTime: string
}

export async function POST(request: NextRequest) {
  try {
    const data: AppointmentData = await request.json()

    // Validation
    const required = ['firstName', 'lastName', 'email', 'consultationType']
    for (const field of required) {
      if (!data[field as keyof AppointmentData]) {
        return NextResponse.json(
          { error: `${field} is required` },
          { status: 400 }
        )
      }
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(data.email)) {
      return NextResponse.json(
        { error: 'Invalid email address' },
        { status: 400 }
      )
    }

    // Here you would:
    // 1. Save to database
    // 2. Send confirmation emails
    // 3. Create calendar events
    // 4. Send SMS notifications

    // For now, we'll simulate success
    console.log('Appointment request received:', data)

    // TODO: Implement email sending (requires nodemailer or similar)
    // TODO: Implement calendar integration
    // TODO: Implement database storage

    return NextResponse.json({ 
      success: true, 
      message: 'Appointment request received! We will contact you within 24 hours to confirm.',
      appointmentId: `APT-${Date.now()}`
    })

  } catch (error) {
    console.error('Appointment booking error:', error)
    return NextResponse.json(
      { error: 'Failed to book appointment. Please try again.' },
      { status: 500 }
    )
  }
}