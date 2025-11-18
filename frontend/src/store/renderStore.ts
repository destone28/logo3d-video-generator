import { create } from 'zustand'
import type { JobStatusResponse } from '../types'

interface RenderState {
  currentJob: JobStatusResponse | null
  isRendering: boolean
  renderHistory: JobStatusResponse[]
  setCurrentJob: (job: JobStatusResponse | null) => void
  setIsRendering: (isRendering: boolean) => void
  addToHistory: (job: JobStatusResponse) => void
  setHistory: (history: JobStatusResponse[]) => void
  reset: () => void
}

export const useRenderStore = create<RenderState>((set) => ({
  currentJob: null,
  isRendering: false,
  renderHistory: [],
  setCurrentJob: (job) => set({ currentJob: job }),
  setIsRendering: (isRendering) => set({ isRendering }),
  addToHistory: (job) =>
    set((state) => ({
      renderHistory: [job, ...state.renderHistory].slice(0, 10),
    })),
  setHistory: (history) => set({ renderHistory: history }),
  reset: () =>
    set({
      currentJob: null,
      isRendering: false,
    }),
}))
