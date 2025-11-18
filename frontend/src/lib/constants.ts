export const APP_NAME = import.meta.env.VITE_APP_NAME || '3D Logo Video Generator'
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || '1.0.0'
export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const MAX_FILE_SIZE = 10 * 1024 * 1024 // 10MB
export const ALLOWED_FILE_TYPES = ['image/png', 'image/jpeg', 'image/jpg', 'image/svg+xml']
export const ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.svg']

export const DEFAULT_RENDER_CONFIG = {
  preset: 'classic_spin',
  duration: 5.0,
  speed: 1.0,
  lighting: 'soft',
  background: {
    type: 'solid' as const,
    color: '#ffffff',
  },
  extrusion: 0.5,
  resolution: '1080p' as const,
  fps: 30 as const,
  quality: 'standard' as const,
}

export const RESOLUTION_OPTIONS = [
  { value: '1080p', label: '1080p (1920x1080)' },
  { value: '4K', label: '4K (3840x2160)' },
]

export const FPS_OPTIONS = [
  { value: 24, label: '24 FPS (Cinematic)' },
  { value: 30, label: '30 FPS (Standard)' },
  { value: 60, label: '60 FPS (Smooth)' },
]

export const QUALITY_OPTIONS = [
  { value: 'standard', label: 'Standard' },
  { value: 'high', label: 'High Quality' },
]

export const BACKGROUND_TYPES = [
  { value: 'solid', label: 'Solid Color' },
  { value: 'gradient', label: 'Gradient' },
  { value: 'transparent', label: 'Transparent' },
  { value: 'hdri', label: 'HDRI Environment' },
]

export const POLL_INTERVAL = 2000 // 2 seconds
export const MAX_POLL_ATTEMPTS = 600 // 20 minutes max (600 * 2s)
