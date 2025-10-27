import React from "react"

export const dynamic = "force-dynamic"

async function getHealth() {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || ''}/api/ml-health`, {
      // Ensure fresh read from the ML service
      cache: 'no-store',
      headers: { 'accept': 'application/json' }
    })
    if (!res.ok) throw new Error(`ml-health returned ${res.status}`)
    return await res.json()
  } catch (e: any) {
    return { status: 'error', error: e?.message || String(e) }
  }
}

export default async function MlStatusPage() {
  const data = await getHealth()
  const ok = data?.status === 'ok'
  const ml = ok ? data.ml : null

  return (
    <main className="mx-auto max-w-3xl px-4 py-10">
      <h1 className="text-2xl font-semibold mb-6">ML Engine Status</h1>

      {!ok && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-800 mb-6">
          <p className="font-medium mb-1">ML service not reachable</p>
          <p className="text-sm">{data?.error || 'Unknown error'}.</p>
          <ul className="list-disc ml-6 mt-3 text-sm">
            <li>Ensure the ML Flask server is running on port 5000</li>
            <li>Check http://localhost:5000/health in a browser</li>
            <li>Then refresh this page</li>
          </ul>
        </div>
      )}

      {ok && (
        <div className="rounded-lg border p-4 bg-white">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <div className="text-gray-500">Service</div>
              <div className="font-medium">Healthy</div>
            </div>
            <div>
              <div className="text-gray-500">Engine</div>
              <div className="font-medium">{ml?.engine || 'Unknown'}</div>
            </div>
            <div>
              <div className="text-gray-500">Models Loaded</div>
              <div className="font-medium">{ml?.ml_models_loaded ? 'Yes' : 'No'}</div>
            </div>
            <div>
              <div className="text-gray-500">Jewelry Items</div>
              <div className="font-medium">{ml?.jewelry_items ?? 0}</div>
            </div>
            <div>
              <div className="text-gray-500">Diamonds</div>
              <div className="font-medium">{ml?.diamonds ?? 0}</div>
            </div>
          </div>
        </div>
      )}

      <div className="mt-8 text-sm text-gray-600">
        <p>
          This page reads from <code>/api/ml-health</code>, which proxies the Flask ML
          service at <code>http://localhost:5000/health</code>. Use it to verify the ML engine is active
          without showing badges in the chat UI.
        </p>
      </div>
    </main>
  )
}
