import apiClient from './client'
import type {
  UploadResponse,
  RenderConfig,
  JobResponse,
  JobStatusResponse,
  PresetsResponse,
  RenderHistoryItem,
} from '../types'

export const uploadAPI = {
  // Upload logo file
  uploadLogo: async (file: File): Promise<UploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await apiClient.post<UploadResponse>('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  // Remove background from uploaded image
  removeBackground: async (uploadId: string) => {
    const response = await apiClient.post('/upload/remove-background', {
      upload_id: uploadId,
    })
    return response.data
  },

  // Get upload details
  getUpload: async (uploadId: string): Promise<UploadResponse> => {
    const response = await apiClient.get<UploadResponse>(`/upload/${uploadId}`)
    return response.data
  },
}

export const renderAPI = {
  // Get available presets
  getPresets: async (): Promise<PresetsResponse> => {
    const response = await apiClient.get<PresetsResponse>('/render/presets')
    return response.data
  },

  // Create preview render
  createPreview: async (uploadId: string, config: RenderConfig): Promise<JobResponse> => {
    const response = await apiClient.post<JobResponse>('/render/preview', {
      upload_id: uploadId,
      config,
    })
    return response.data
  },

  // Create final render
  createFinalRender: async (uploadId: string, config: RenderConfig): Promise<JobResponse> => {
    const response = await apiClient.post<JobResponse>('/render/final', {
      upload_id: uploadId,
      config,
    })
    return response.data
  },
}

export const jobsAPI = {
  // Get job status
  getJobStatus: async (jobId: string): Promise<JobStatusResponse> => {
    const response = await apiClient.get<JobStatusResponse>(`/jobs/${jobId}`)
    return response.data
  },

  // Cancel job
  cancelJob: async (jobId: string) => {
    const response = await apiClient.delete(`/jobs/${jobId}`)
    return response.data
  },

  // Get render history for an upload
  getRenderHistory: async (uploadId: string, limit: number = 10): Promise<RenderHistoryItem[]> => {
    const response = await apiClient.get<RenderHistoryItem[]>(`/jobs/upload/${uploadId}/history`, {
      params: { limit },
    })
    return response.data
  },

  // List recent jobs
  listJobs: async (status?: string, limit: number = 20): Promise<JobStatusResponse[]> => {
    const response = await apiClient.get<JobStatusResponse[]>('/jobs/', {
      params: { status, limit },
    })
    return response.data
  },
}

export const healthAPI = {
  // Health check
  healthCheck: async () => {
    const response = await apiClient.get('/health/')
    return response.data
  },

  // Detailed health check
  detailedHealthCheck: async () => {
    const response = await apiClient.get('/health/detailed')
    return response.data
  },
}
