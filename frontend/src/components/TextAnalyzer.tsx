import type { AnalysisMode } from '../types/sentiment'

interface TextAnalyzerProps { text: string; setText: (value: string) => void; mode: AnalysisMode; setMode: (value: AnalysisMode) => void; onAnalyze: () => void; loading: boolean }
const modes: { value: AnalysisMode; label: string; description: string }[] = [
  { value: 'gemini', label: 'Gemini AI', description: 'Advanced AI analysis' },
  { value: 'public', label: 'Public API', description: 'External classifier' },
  { value: 'compare', label: 'Compare both', description: 'Compare providers' },
]

export default function TextAnalyzer({ text, setText, mode, setMode, onAnalyze, loading }: TextAnalyzerProps) {
  const validText = text.trim().length > 0 && text.length <= 5000
  return (
    <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
      <h2 className="text-xl font-bold text-slate-900">Analyze your text</h2><p className="mt-1 text-sm text-slate-500">Enter a review, comment, or message to discover its sentiment.</p>
      <div className="mt-6"><label htmlFor="sentiment-text" className="mb-2 block text-sm font-semibold text-slate-700">Your text</label><textarea id="sentiment-text" value={text} onChange={(event) => setText(event.target.value)} placeholder="Example: This product is amazing! The quality is excellent..." rows={7} maxLength={5000} className="w-full resize-y rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm leading-7 text-slate-800 outline-none transition placeholder:text-slate-400 focus:border-blue-500 focus:bg-white focus:ring-4 focus:ring-blue-50" /><div className="mt-2 flex justify-between text-xs text-slate-400"><span>Maximum 5,000 characters</span><span className={text.length >= 4900 ? 'font-semibold text-amber-600' : ''}>{text.length}/5000</span></div></div>
      <fieldset className="mt-7"><legend className="mb-3 text-sm font-semibold text-slate-700">Analysis provider</legend><div className="grid gap-3 sm:grid-cols-3">{modes.map((item) => <button key={item.value} type="button" aria-pressed={mode === item.value} onClick={() => setMode(item.value)} className={`rounded-xl border p-4 text-left transition ${mode === item.value ? 'border-blue-500 bg-blue-50 ring-2 ring-blue-100' : 'border-slate-200 bg-white hover:border-slate-300'}`}><p className="text-sm font-semibold text-slate-900">{item.label}</p><p className="mt-1 text-xs text-slate-500">{item.description}</p></button>)}</div></fieldset>
      <button type="button" onClick={onAnalyze} disabled={!validText || loading} className="mt-7 flex w-full items-center justify-center gap-2 rounded-xl bg-blue-600 px-5 py-3.5 text-sm font-semibold text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-slate-300">{loading ? <><span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />Analyzing...</> : <>✦ Analyze sentiment</>}</button>
    </section>
  )
}
