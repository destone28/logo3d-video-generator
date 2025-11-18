import { create } from 'zustand'
import type { UploadResponse } from '../types'

interface UploadState {
  currentUpload: UploadResponse | null
  isUploading: boolean
  uploadProgress: number
  error: string | null
  setCurrentUpload: (upload: UploadResponse | null) => void
  setIsUploading: (isUploading: boolean) => void
  setUploadProgress: (progress: number) => void
  setError: (error: string | null) => void
  reset: () => void
}

export const useUploadStore = create<UploadState>((set) => ({
  currentUpload: null,
  isUploading: false,
  uploadProgress: 0,
  error: null,
  setCurrentUpload: (upload) => set({ currentUpload: upload }),
  setIsUploading: (isUploading) => set({ isUploading }),
  setUploadProgress: (progress) => set({ uploadProgress: progress }),
  setError: (error) => set({ error }),
  reset: () =>
    set({
      currentUpload: null,
      isUploading: false,
      uploadProgress: 0,
      error: null,
    }),
}))
