import { create } from 'zustand'
import type { RenderConfig, PresetsResponse } from '../types'
import { DEFAULT_RENDER_CONFIG } from '../lib/constants'

interface ConfigState {
  config: RenderConfig
  presets: PresetsResponse | null
  setConfig: (config: Partial<RenderConfig>) => void
  setPresets: (presets: PresetsResponse) => void
  resetConfig: () => void
}

export const useConfigStore = create<ConfigState>((set) => ({
  config: DEFAULT_RENDER_CONFIG,
  presets: null,
  setConfig: (newConfig) =>
    set((state) => ({
      config: { ...state.config, ...newConfig },
    })),
  setPresets: (presets) => set({ presets }),
  resetConfig: () => set({ config: DEFAULT_RENDER_CONFIG }),
}))
