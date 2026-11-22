export type Sentiment = 'positive' | 'negative' | 'neutral'
export type AnalysisMode = 'gemini' | 'public' | 'compare'

export interface GeminiResult {
  sentiment: Sentiment
  confidence: number
  explanation: string
  keywords: string[]
}

export interface PublicResult {
  sentiment: Sentiment
  confidence: number
  probabilities: { positive: number; negative: number; neutral: number }
}
