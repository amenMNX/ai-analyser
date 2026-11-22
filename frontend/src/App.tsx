import { useEffect, useState } from 'react'
import Dashboard from './Dashboard'

interface HealthResponse {
  status: string
  service: string
}

const apiUrl = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const checkBackend = async () => {
      try {
        const response = await fetch(`${apiUrl}/api/health`)
        if (!response.ok) throw new Error('Backend request failed')
        setHealth((await response.json()) as HealthResponse)
      } catch {
        setError('Cannot connect to the backend.')
      }
    }

    void checkBackend()
  }, [])

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-50 p-6">
      <section className="w-full max-w-lg rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <p className="text-sm font-semibold tracking-wide text-blue-600">AI SENTIMENT ANALYZER</p>
        <h1 className="mt-3 text-3xl font-bold text-slate-900">Project initialized.</h1>
        <p className="mt-2 text-slate-500">Welcome to your AI-powered sentiment analysis platform.</p>

        <div className="mt-8 rounded-xl bg-slate-50 p-4">
          <p className="font-semibold text-slate-700">Backend connection</p>
          {health ? (
            <p className="mt-2 text-sm text-emerald-600">● Connected — {health.status}</p>
          ) : error ? (
            <p className="mt-2 text-sm text-red-600">● {error}</p>
          ) : (
            <p className="mt-2 text-sm text-amber-600">● Connecting...</p>
          )}
        </div>
      </section>
    </main>
  )
}

export default Dashboard
