export interface UploadResponse {
  upload_id: string
  filename: string
  thumbnail_url: string | null
  original_url: string
  width: number
  height: number
  file_size: number
  has_transparency: boolean
  background_removed: boolean
  created_at: string
}

export interface BackgroundConfig {
  type: 'solid' | 'gradient' | 'transparent' | 'hdri'
  color?: string
  gradient_start?: string
  gradient_end?: string
  hdri_name?: string
}

export interface RenderConfig {
  preset: string
  duration: number
  speed: number
  lighting: string
  background: BackgroundConfig
  extrusion: number
  resolution: '1080p' | '4K'
  fps: 24 | 30 | 60
  quality: 'standard' | 'high'
}

export interface JobResponse {
  job_id: string
  status: string
  progress: number
  estimated_time?: number
  result_url?: string
  thumbnail_url?: string
  error?: string
}

export interface JobStatusResponse {
  job_id: string
  status: string
  progress: number
  estimated_remaining?: number
  result_url?: string
  thumbnail_url?: string
  error_message?: string
  created_at: string
  started_at?: string
  completed_at?: string
}

export interface AnimationPreset {
  name: string
  description: string
}

export interface PresetsResponse {
  animations: Record<string, AnimationPreset>
  lighting: string[]
}

export interface RenderHistoryItem {
  render_id: string
  created_at: string
  status: string
  config: RenderConfig
  thumbnail_url?: string
  video_url?: string
  duration: number
  resolution: string
  file_size?: number
}
