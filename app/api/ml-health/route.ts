import { NextResponse } from 'next/server'

// Ensure this route runs in the Node runtime (not Edge) so it can reach localhost services
export const runtime = 'nodejs'

// Simple in-memory cache to avoid returning 502 on brief ML service blips.
// Cache duration (ms)
const CACHE_TTL = 30_000
let cachedMl: any = null
let cachedAt = 0

export async function GET() {
  const now = Date.now()

  // If cache is fresh, return it immediately
  if (cachedMl && (now - cachedAt) < CACHE_TTL) {
    return NextResponse.json({ status: 'ok', ml: cachedMl, cached: true })
  }

  const endpoints = ['http://127.0.0.1:5000/health', 'http://localhost:5000/health']
  let lastError: any = null

  // helper: fetch with timeout
  const fetchWithTimeout = async (url: string, ms = 3000) => {
    const controller = new AbortController()
    const id = setTimeout(() => controller.abort(), ms)
    try {
      const res = await fetch(url, { cache: 'no-store', signal: controller.signal })
      clearTimeout(id)
      return res
    } catch (e) {
      clearTimeout(id)
      throw e
    }
  }

  // try each endpoint with limited retries and backoff
  for (const url of endpoints) {
    let attempt = 0
    const maxAttempts = 2
    while (attempt < maxAttempts) {
      attempt++
      try {
        console.log('[ml-health] trying', url, 'attempt', attempt)
        const res = await fetchWithTimeout(url, 3000)
        if (!res.ok) {
          lastError = { url, status: res.status }
          console.log('[ml-health] endpoint returned non-OK', url, res.status)
          // short backoff before retry
          await new Promise(r => setTimeout(r, 150 * attempt))
          continue
        }
        const data = await res.json()
        // Update cache
        cachedMl = data
        cachedAt = Date.now()
        return NextResponse.json({ status: 'ok', ml: data, cached: false })
      } catch (err) {
        lastError = { url, message: (err as Error).message }
        console.log('[ml-health] fetch error for', url, (err as Error).message)
        // short backoff before retry
        await new Promise(r => setTimeout(r, 150 * attempt))
      }
    }
  }

  // If we have cached data, return it with cached:true and a warning
  if (cachedMl) {
    return NextResponse.json({ status: 'ok', ml: cachedMl, cached: true, warning: lastError }, { status: 200 })
  }

  // No cache and both endpoints failed
  return NextResponse.json({ status: 'unavailable', error: lastError }, { status: 502 })
}
