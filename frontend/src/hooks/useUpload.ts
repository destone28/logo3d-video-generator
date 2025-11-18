import { useMutation } from '@tanstack/react-query'
import { uploadAPI } from '../api/endpoints'
import { useUploadStore } from '../store/uploadStore'

export function useUpload() {
  const { setCurrentUpload, setIsUploading, setError } = useUploadStore()

  const uploadMutation = useMutation({
    mutationFn: (file: File) => uploadAPI.uploadLogo(file),
    onMutate: () => {
      setIsUploading(true)
      setError(null)
    },
    onSuccess: (data) => {
      setCurrentUpload(data)
      setIsUploading(false)
    },
    onError: (error: any) => {
      setError(error.response?.data?.detail || 'Upload failed')
      setIsUploading(false)
    },
  })

  const removeBackgroundMutation = useMutation({
    mutationFn: (uploadId: string) => uploadAPI.removeBackground(uploadId),
    onSuccess: (_data, uploadId) => {
      // Refetch upload to get updated data
      uploadAPI.getUpload(uploadId).then(setCurrentUpload)
    },
    onError: (error: any) => {
      setError(error.response?.data?.detail || 'Background removal failed')
    },
  })

  return {
    uploadFile: uploadMutation.mutate,
    removeBackground: removeBackgroundMutation.mutate,
    isUploading: uploadMutation.isPending,
    isRemovingBackground: removeBackgroundMutation.isPending,
  }
}
