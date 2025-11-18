import { useQuery } from '@tanstack/react-query'
import { jobsAPI } from '../api/endpoints'
import { useRenderStore } from '../store/renderStore'
import { POLL_INTERVAL } from '../lib/constants'
import { useEffect } from 'react'

export function useJobStatus(jobId: string | null, enabled: boolean = true) {
  const { setCurrentJob, setIsRendering } = useRenderStore()

  const query = useQuery({
    queryKey: ['job-status', jobId],
    queryFn: () => jobsAPI.getJobStatus(jobId!),
    enabled: enabled && !!jobId,
    refetchInterval: (data) => {
      // Stop polling if job is completed or failed
      if (data && (data.status === 'completed' || data.status === 'failed')) {
        return false
      }
      return POLL_INTERVAL
    },
    refetchIntervalInBackground: true,
  })

  useEffect(() => {
    if (query.data) {
      setCurrentJob(query.data)

      // Update rendering state
      if (query.data.status === 'completed' || query.data.status === 'failed') {
        setIsRendering(false)
      }
    }
  }, [query.data, setCurrentJob, setIsRendering])

  return {
    job: query.data,
    isLoading: query.isLoading,
    error: query.error,
    refetch: query.refetch,
  }
}
