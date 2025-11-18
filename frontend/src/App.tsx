import { useState, useCallback } from 'react'
import { useUpload } from './hooks/useUpload'
import { useRender } from './hooks/useRender'
import { useJobStatus } from './hooks/useJobStatus'
import { useUploadStore } from './store/uploadStore'
import { useConfigStore } from './store/configStore'
import { useRenderStore } from './store/renderStore'
import { formatFileSize, formatDuration, getStatusBadgeColor, downloadFile } from './lib/utils'
import { ALLOWED_FILE_TYPES, MAX_FILE_SIZE } from './lib/constants'

function App() {
  const [dragActive, setDragActive] = useState(false)

  const { currentUpload } = useUploadStore()
  const { config, setConfig } = useConfigStore()
  const { currentJob } = useRenderStore()

  const { uploadFile, removeBackground, isUploading, isRemovingBackground } = useUpload()
  const { createPreview, createRender, isCreatingPreview, isCreatingRender, presets: presetsData } = useRender()

  useJobStatus(currentJob?.job_id || null, !!currentJob)

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0])
    }
  }, [])

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0])
    }
  }, [])

  const handleFile = (file: File) => {
    if (!ALLOWED_FILE_TYPES.includes(file.type)) {
      alert('Invalid file type. Please upload PNG, JPG, or SVG.')
      return
    }
    if (file.size > MAX_FILE_SIZE) {
      alert(`File too large. Maximum size is ${formatFileSize(MAX_FILE_SIZE)}`)
      return
    }
    uploadFile(file)
  }

  const handlePreview = () => {
    if (currentUpload) {
      createPreview({ uploadId: currentUpload.upload_id, config })
    }
  }

  const handleRender = () => {
    if (currentUpload) {
      createRender({ uploadId: currentUpload.upload_id, config })
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-slate-900">3D Logo Video Generator</h1>
          <p className="text-slate-600 mt-1">Transform your 2D logos into stunning 3D animated videos</p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Upload & Configuration */}
          <div className="space-y-6">
            {/* Upload Section */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">1. Upload Logo</h2>

              {!currentUpload ? (
                <div
                  className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition ${
                    dragActive ? 'border-blue-500 bg-blue-50' : 'border-slate-300 hover:border-blue-400'
                  }`}
                  onDragEnter={handleDrag}
                  onDragLeave={handleDrag}
                  onDragOver={handleDrag}
                  onDrop={handleDrop}
                  onClick={() => document.getElementById('file-input')?.click()}
                >
                  <div className="text-6xl mb-4">📁</div>
                  <p className="text-lg font-medium text-slate-700">
                    {isUploading ? 'Uploading...' : 'Drop your logo here or click to browse'}
                  </p>
                  <p className="text-sm text-slate-500 mt-2">PNG, JPG, SVG up to {formatFileSize(MAX_FILE_SIZE)}</p>
                  <input
                    id="file-input"
                    type="file"
                    className="hidden"
                    accept={ALLOWED_FILE_TYPES.join(',')}
                    onChange={handleChange}
                    disabled={isUploading}
                  />
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex items-start gap-4">
                    {currentUpload.thumbnail_url && (
                      <img
                        src={currentUpload.thumbnail_url}
                        alt="Logo preview"
                        className="w-32 h-32 object-contain border border-slate-200 rounded"
                      />
                    )}
                    <div className="flex-1">
                      <p className="font-medium">{currentUpload.filename}</p>
                      <p className="text-sm text-slate-600">
                        {currentUpload.width} × {currentUpload.height} • {formatFileSize(currentUpload.file_size)}
                      </p>
                      <button
                        onClick={() => removeBackground(currentUpload.upload_id)}
                        disabled={isRemovingBackground || currentUpload.background_removed}
                        className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:bg-gray-300 text-sm"
                      >
                        {isRemovingBackground ? 'Removing...' : currentUpload.background_removed ? 'Background Removed' : 'Remove Background'}
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Configuration Section */}
            {currentUpload && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold mb-4">2. Configure Animation</h2>

                <div className="space-y-4">
                  {/* Animation Preset */}
                  <div>
                    <label className="block text-sm font-medium mb-2">Animation Preset</label>
                    <select
                      value={config.preset}
                      onChange={(e) => setConfig({ preset: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-md"
                    >
                      {presetsData && presetsData.animations && Object.entries(presetsData.animations).map(([key, preset]: [string, any]) => (
                        <option key={key} value={key}>
                          {preset.name} - {preset.description}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Lighting */}
                  <div>
                    <label className="block text-sm font-medium mb-2">Lighting</label>
                    <select
                      value={config.lighting}
                      onChange={(e) => setConfig({ lighting: e.target.value })}
                      className="w-full px-3 py-2 border border-slate-300 rounded-md"
                    >
                      {presetsData && presetsData.lighting && Array.isArray(presetsData.lighting) && presetsData.lighting.map((light: string) => (
                        <option key={light} value={light}>
                          {light.charAt(0).toUpperCase() + light.slice(1)}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Duration */}
                  <div>
                    <label className="block text-sm font-medium mb-2">Duration: {config.duration}s</label>
                    <input
                      type="range"
                      min="3"
                      max="15"
                      step="0.5"
                      value={config.duration}
                      onChange={(e) => setConfig({ duration: parseFloat(e.target.value) })}
                      className="w-full"
                    />
                  </div>

                  {/* Extrusion */}
                  <div>
                    <label className="block text-sm font-medium mb-2">3D Depth: {config.extrusion.toFixed(1)}</label>
                    <input
                      type="range"
                      min="0.1"
                      max="2"
                      step="0.1"
                      value={config.extrusion}
                      onChange={(e) => setConfig({ extrusion: parseFloat(e.target.value) })}
                      className="w-full"
                    />
                  </div>

                  {/* Resolution & Quality */}
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">Resolution</label>
                      <select
                        value={config.resolution}
                        onChange={(e) => setConfig({ resolution: e.target.value as '1080p' | '4K' })}
                        className="w-full px-3 py-2 border border-slate-300 rounded-md"
                      >
                        <option value="1080p">1080p</option>
                        <option value="4K">4K</option>
                      </select>
                    </div>
                    <div>
                      <label className="block text-sm font-medium mb-2">Quality</label>
                      <select
                        value={config.quality}
                        onChange={(e) => setConfig({ quality: e.target.value as 'standard' | 'high' })}
                        className="w-full px-3 py-2 border border-slate-300 rounded-md"
                      >
                        <option value="standard">Standard</option>
                        <option value="high">High</option>
                      </select>
                    </div>
                  </div>

                  {/* Action Buttons */}
                  <div className="flex gap-3 pt-4">
                    <button
                      onClick={handlePreview}
                      disabled={isCreatingPreview || isCreatingRender}
                      className="flex-1 px-6 py-3 bg-slate-600 text-white rounded-lg hover:bg-slate-700 disabled:bg-gray-300 font-medium"
                    >
                      {isCreatingPreview ? 'Creating...' : 'Preview (Low Quality)'}
                    </button>
                    <button
                      onClick={handleRender}
                      disabled={isCreatingPreview || isCreatingRender}
                      className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 font-medium"
                    >
                      {isCreatingRender ? 'Creating...' : 'Final Render'}
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right Column - Preview & Status */}
          <div className="space-y-6">
            {currentJob && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-xl font-semibold mb-4">Render Status</h2>

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-medium">Status:</span>
                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusBadgeColor(currentJob.status)}`}>
                      {currentJob.status.toUpperCase()}
                    </span>
                  </div>

                  {currentJob.status === 'processing' && (
                    <div>
                      <div className="flex justify-between text-sm mb-2">
                        <span>Progress</span>
                        <span>{currentJob.progress}%</span>
                      </div>
                      <div className="w-full bg-slate-200 rounded-full h-3">
                        <div
                          className="bg-blue-600 h-3 rounded-full transition-all duration-300"
                          style={{ width: `${currentJob.progress}%` }}
                        />
                      </div>
                      {currentJob.estimated_remaining && (
                        <p className="text-sm text-slate-600 mt-2">
                          Estimated time remaining: {formatDuration(currentJob.estimated_remaining)}
                        </p>
                      )}
                    </div>
                  )}

                  {currentJob.status === 'completed' && currentJob.result_url && (
                    <div className="space-y-4">
                      <video
                        src={currentJob.result_url}
                        controls
                        className="w-full rounded-lg border border-slate-200"
                      />
                      <button
                        onClick={() => downloadFile(currentJob.result_url!, 'logo-animation.mp4')}
                        className="w-full px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 font-medium"
                      >
                        Download Video
                      </button>
                    </div>
                  )}

                  {currentJob.status === 'failed' && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                      <p className="text-red-800 font-medium">Render Failed</p>
                      <p className="text-red-600 text-sm mt-1">{currentJob.error_message || 'An error occurred'}</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {!currentJob && currentUpload && (
              <div className="bg-white rounded-lg shadow-md p-6 text-center">
                <div className="text-6xl mb-4">🎬</div>
                <h3 className="text-xl font-semibold mb-2">Ready to Render</h3>
                <p className="text-slate-600">
                  Configure your animation settings and click Preview or Final Render to get started
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 bg-white border-t border-slate-200">
        <div className="container mx-auto px-4 py-6 text-center text-slate-600">
          <p>3D Logo Video Generator v1.0.0</p>
          <p className="text-sm mt-1">Powered by Blender, FastAPI, and React</p>
        </div>
      </footer>
    </div>
  )
}

export default App
