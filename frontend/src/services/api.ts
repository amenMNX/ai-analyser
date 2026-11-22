import type { GeminiResult, PublicResult } from '../types/sentiment'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

async function request<T>(endpoint: string, text: string): Promise<T> {
  const response = await fetch(`${API_URL}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
  if (!response.ok) {
    let message = `Request failed (${response.status})`
    try { message = ((await response.json()) as { detail?: string }).detail ?? message } catch { /* use default */ }
    throw new Error(message)
  }
  return (await response.json()) as T
}

export function analyzeWithGemini(text: string): Promise<GeminiResult> { return request<GeminiResult>('/api/analyze', text) }
export function analyzeWithPublicAPI(text: string): Promise<PublicResult> { return request<PublicResult>('/api/analyze/public', text) }
export async function checkBackend(): Promise<boolean> {
  try { return (await fetch(`${API_URL}/api/health`)).ok } catch { return false }
}
