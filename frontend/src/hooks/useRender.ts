import { useMutation, useQuery } from '@tanstack/react-query'
import { useEffect } from 'react'
import { renderAPI } from '../api/endpoints'
import { useConfigStore } from '../store/configStore'
import { useRenderStore } from '../store/renderStore'
import type { RenderConfig } from '../types'

export function useRender() {
  const { setPresets } = useConfigStore()
  const { setCurrentJob, setIsRendering } = useRenderStore()

  // Fetch presets
  const presetsQuery = useQuery({
    queryKey: ['presets'],
    queryFn: renderAPI.getPresets,
    staleTime: Infinity, // Presets don't change
  })

  // Update presets in store when data changes
  useEffect(() => {
    if (presetsQuery.data) {
      setPresets(presetsQuery.data)
    }
  }, [presetsQuery.data, setPresets])

  // Create preview
  const previewMutation = useMutation({
    mutationFn: ({ uploadId, config }: { uploadId: string; config: RenderConfig }) =>
      renderAPI.createPreview(uploadId, config),
    onMutate: () => {
      setIsRendering(true)
    },
    onSuccess: (data) => {
      setCurrentJob({
        ...data,
        created_at: new Date().toISOString(),
      })
    },
    onError: () => {
      setIsRendering(false)
    },
  })

  // Create final render
  const renderMutation = useMutation({
    mutationFn: ({ uploadId, config }: { uploadId: string; config: RenderConfig }) =>
      renderAPI.createFinalRender(uploadId, config),
    onMutate: () => {
      setIsRendering(true)
    },
    onSuccess: (data) => {
      setCurrentJob({
        ...data,
        created_at: new Date().toISOString(),
      })
    },
    onError: () => {
      setIsRendering(false)
    },
  })

  return {
    presets: presetsQuery.data,
    isLoadingPresets: presetsQuery.isLoading,
    createPreview: previewMutation.mutate,
    createRender: renderMutation.mutate,
    isCreatingPreview: previewMutation.isPending,
    isCreatingRender: renderMutation.isPending,
  }
}
