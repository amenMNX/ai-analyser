import { useEffect, useState } from 'react'

import Header from './components/Header'
import SentimentResult from './components/SentimentResult'
import TextAnalyzer from './components/TextAnalyzer'
import { analyzeWithGemini, analyzeWithPublicAPI, checkBackend } from './services/api'
import type { AnalysisMode, GeminiResult, PublicResult } from './types/sentiment'

function Dashboard() {
  const [text, setText] = useState('')
  const [mode, setMode] = useState<AnalysisMode>('compare')
  const [connected, setConnected] = useState<boolean | null>(null)
  const [geminiResult, setGeminiResult] = useState<GeminiResult | null>(null)
  const [publicResult, setPublicResult] = useState<PublicResult | null>(null)
  const [geminiError, setGeminiError] = useState<string | null>(null)
  const [publicError, setPublicError] = useState<string | null>(null)
  const [geminiLoading, setGeminiLoading] = useState(false)
  const [publicLoading, setPublicLoading] = useState(false)

  useEffect(() => { void checkBackend().then(setConnected) }, [])

  const handleAnalyze = async () => {
    if (!text.trim() || text.length > 5000 || geminiLoading || publicLoading) return
    setGeminiResult(null); setPublicResult(null); setGeminiError(null); setPublicError(null)
    const tasks: Promise<void>[] = []
    if (mode === 'gemini' || mode === 'compare') {
      setGeminiLoading(true)
      tasks.push(analyzeWithGemini(text).then(setGeminiResult).catch((error: unknown) => setGeminiError(error instanceof Error ? error.message : 'Gemini analysis failed.')).finally(() => setGeminiLoading(false)))
    }
    if (mode === 'public' || mode === 'compare') {
      setPublicLoading(true)
      tasks.push(analyzeWithPublicAPI(text).then(setPublicResult).catch((error: unknown) => setPublicError(error instanceof Error ? error.message : 'Public API analysis failed.')).finally(() => setPublicLoading(false)))
    }
    await Promise.allSettled(tasks)
  }

  const showGemini = mode === 'gemini' || mode === 'compare'
  const showPublic = mode === 'public' || mode === 'compare'
  const hasResults = Boolean(geminiResult || publicResult || geminiError || publicError || geminiLoading || publicLoading)
  const loading = geminiLoading || publicLoading

  return <div className="min-h-screen bg-slate-50">
    <Header connected={connected} />
    <main className="mx-auto max-w-6xl px-5 py-10 lg:px-8">
      <div className="mb-8"><p className="text-sm font-semibold uppercase tracking-wider text-blue-600">Sentiment intelligence</p><h1 className="mt-2 text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">Understand what people feel.</h1><p className="mt-3 max-w-2xl text-slate-500">Analyze text with AI and compare sentiment results from independent external services.</p></div>
      <TextAnalyzer text={text} setText={setText} mode={mode} setMode={setMode} onAnalyze={() => void handleAnalyze()} loading={loading} />
      {hasResults && <section className="mt-10"><div className="mb-5"><h2 className="text-xl font-bold text-slate-900">Analysis results</h2><p className="mt-1 text-sm text-slate-500">Results returned by the selected providers.</p></div><div className="grid gap-5 md:grid-cols-2">{showGemini && <SentimentResult title="Google Gemini AI" provider="gemini" result={geminiResult} error={geminiError} loading={geminiLoading} />}{showPublic && <SentimentResult title="Text-Processing API" provider="public" result={publicResult} error={publicError} loading={publicLoading} />}</div></section>}
      <footer className="mt-16 border-t border-slate-200 py-6 text-center text-xs text-slate-400">AI Sentiment Analyzer · Powered by FastAPI and external AI services</footer>
    </main>
  </div>
}

export default Dashboard
