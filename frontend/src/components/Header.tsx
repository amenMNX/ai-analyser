interface HeaderProps { connected: boolean | null }

export default function Header({ connected }: HeaderProps) {
  const label = connected === null ? 'Checking backend...' : connected ? 'Backend connected' : 'Backend unavailable'
  return (
    <header className="border-b border-slate-200 bg-white px-6 py-5 lg:px-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div><div className="flex items-center gap-3"><div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 text-xl text-white">✦</div><span className="text-lg font-bold text-slate-900">SentimentAI</span></div><p className="mt-2 text-sm text-slate-500">AI-powered text sentiment analysis</p></div>
        <div className="flex w-fit items-center gap-2 rounded-full border border-slate-200 px-3 py-2 text-sm"><span className={`h-2.5 w-2.5 rounded-full ${connected ? 'bg-emerald-500' : connected === false ? 'bg-red-500' : 'bg-amber-400'}`} /><span className="text-slate-600">{label}</span></div>
      </div>
    </header>
  )
}
