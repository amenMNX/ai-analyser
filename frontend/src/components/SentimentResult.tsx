import type { GeminiResult, PublicResult, Sentiment } from '../types/sentiment'

interface Props { title: string; provider: 'gemini' | 'public'; result: GeminiResult | PublicResult | null; error: string | null; loading: boolean }
const sentimentStyles: Record<Sentiment, string> = { positive: 'bg-emerald-50 text-emerald-700 border-emerald-200', negative: 'bg-red-50 text-red-700 border-red-200', neutral: 'bg-slate-100 text-slate-700 border-slate-200' }

export default function SentimentResult({ title, provider, result, error, loading }: Props) {
  if (loading) return <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><p className="font-semibold text-slate-900">{title}</p><p className="mt-4 animate-pulse text-sm text-blue-600">Analyzing your text...</p></div>
  if (error) return <div className="rounded-2xl border border-red-200 bg-white p-6 shadow-sm"><p className="font-semibold text-slate-900">{title}</p><p className="mt-3 text-sm text-red-600">{error}</p></div>
  if (!result) return null
  const confidence = Math.min(1, Math.max(0, result.confidence))
  const gemini = provider === 'gemini' ? result as GeminiResult : null
  const publicResult = provider === 'public' ? result as PublicResult : null
  return (
    <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><p className="text-sm font-semibold text-slate-500">{title}</p><span className={`mt-5 inline-flex rounded-full border px-4 py-2 text-sm font-bold capitalize ${sentimentStyles[result.sentiment]}`}>{result.sentiment}</span>
      <div className="mt-6"><div className="flex justify-between text-sm"><span className="font-medium text-slate-600">Confidence</span><span className="font-bold text-slate-900">{(confidence * 100).toFixed(1)}%</span></div><div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-blue-600 transition-all" style={{ width: `${confidence * 100}%` }} /></div></div>
      {gemini && <><div className="mt-6 border-t border-slate-100 pt-5"><h3 className="text-sm font-semibold text-slate-800">AI explanation</h3><p className="mt-2 text-sm leading-6 text-slate-600">{gemini.explanation}</p></div><div className="mt-5"><h3 className="text-sm font-semibold text-slate-800">Important keywords</h3><div className="mt-3 flex flex-wrap gap-2">{gemini.keywords.length ? gemini.keywords.map((keyword, index) => <span key={`${keyword}-${index}`} className="rounded-lg bg-blue-50 px-3 py-1.5 text-xs font-medium text-blue-700">{keyword}</span>) : <span className="text-sm text-slate-400">No keywords returned.</span>}</div></div></>}
      {publicResult && <div className="mt-6 border-t border-slate-100 pt-5"><h3 className="text-sm font-semibold text-slate-800">Sentiment probabilities</h3><div className="mt-4 space-y-3">{Object.entries(publicResult.probabilities).map(([label, value]) => <div key={label}><div className="flex justify-between text-xs capitalize text-slate-600"><span>{label}</span><span>{(value * 100).toFixed(1)}%</span></div><div className="mt-1 h-2 rounded-full bg-slate-100"><div className="h-2 rounded-full bg-blue-500" style={{ width: `${Math.min(1, Math.max(0, value)) * 100}%` }} /></div></div>)}</div></div>}
    </article>
  )
}
