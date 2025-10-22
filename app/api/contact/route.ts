import { NextRequest, NextResponse } from 'next/server'

// Email configuration - will be implemented when environment variables are set up
const sendEmail = async (to: string, subject: string, html: string) => {
  // TODO: Implement with nodemailer when EMAIL_USER and EMAIL_PASS are configured
  console.log('Email would be sent to:', to, 'Subject:', subject)
  return true // Simulate success for now
}

export async function POST(request: NextRequest) {
  try {
    const { name, email, message } = await request.json()

    // Validation
    if (!name || !email || !message) {
      return NextResponse.json(
        { error: 'All fields are required' },
        { status: 400 }
      )
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: 'Invalid email address' },
        { status: 400 }
      )
    }

    // Send email to business
    await sendEmail(
      'hello@ornamenttech.com',
      `New Contact Form Submission from ${name}`,
      `
        <h3>New Contact Form Submission</h3>
        <p><strong>Name:</strong> ${name}</p>
        <p><strong>Email:</strong> ${email}</p>
        <p><strong>Message:</strong></p>
        <p>${message.replace(/\n/g, '<br>')}</p>
        <p><strong>Submitted:</strong> ${new Date().toLocaleString()}</p>
      `
    )

    // Send auto-response to customer
    await sendEmail(
      email,
      'Thank you for contacting Ornament Tech',
      `
        <h3>Thank you for your message, ${name}!</h3>
        <p>We've received your inquiry and will get back to you within 24 hours.</p>
        <p>For urgent matters, please call us at +44 20 8154 9500.</p>
        <br>
        <p>Best regards,<br>The Ornament Tech Team</p>
      `
    )

    return NextResponse.json({ 
      success: true, 
      message: 'Thank you for your message! We will get back to you soon.' 
    })

  } catch (error) {
    console.error('Contact form error:', error)
    return NextResponse.json(
      { error: 'Failed to send message. Please try again.' },
      { status: 500 }
    )
  }
}