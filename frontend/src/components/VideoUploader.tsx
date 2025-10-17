'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, Film, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import { AnalysisData } from '@/types'

interface VideoUploaderProps {
  onAnalysisComplete: (data: AnalysisData) => void
  isAnalyzing: boolean
  setIsAnalyzing: (val: boolean) => void
}

export default function VideoUploader({ onAnalysisComplete, isAnalyzing, setIsAnalyzing }: VideoUploaderProps) {
  const [uploadProgress, setUploadProgress] = useState(0)
  const [analysisStage, setAnalysisStage] = useState<string>('')
  const [error, setError] = useState<string>('')
  const [selectedFile, setSelectedFile] = useState<File | null>(null)

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      setSelectedFile(acceptedFiles[0])
      setError('')
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'video/*': ['.mp4', '.mov', '.avi', '.mkv', '.webm']
    },
    maxFiles: 1,
    disabled: isAnalyzing
  })

  const handleAnalyze = async () => {
    if (!selectedFile) return

    setIsAnalyzing(true)
    setError('')
    setUploadProgress(0)
    setAnalysisStage('Uploading video...')

    const formData = new FormData()
    formData.append('video', selectedFile)
    formData.append('use_goal_calibration', 'true')

    try {
      const response = await axios.post<AnalysisData>(
        'http://localhost:8000/api/analyze',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
          onUploadProgress: (progressEvent) => {
            const progress = progressEvent.total 
              ? Math.round((progressEvent.loaded * 50) / progressEvent.total)
              : 0
            setUploadProgress(progress)
            
            if (progress === 50) {
              setAnalysisStage('Detecting ball...')
              setTimeout(() => {
                setUploadProgress(65)
                setAnalysisStage('Tracking trajectory...')
              }, 500)
              setTimeout(() => {
                setUploadProgress(80)
                setAnalysisStage('Calculating metrics...')
              }, 1500)
              setTimeout(() => {
                setUploadProgress(95)
                setAnalysisStage('Finalizing analysis...')
              }, 2500)
            }
          }
        }
      )

      setUploadProgress(100)
      setAnalysisStage('Complete!')
      
      setTimeout(() => {
        onAnalysisComplete(response.data)
      }, 500)

    } catch (err: any) {
      console.error('Analysis error:', err)
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
      setIsAnalyzing(false)
      setUploadProgress(0)
      setAnalysisStage('')
    }
  }

  return (
    <div className="max-w-4xl mx-auto">
      <AnimatePresence mode="wait">
        {!isAnalyzing ? (
          <motion.div
            key="uploader"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="space-y-6"
          >
            {/* Dropzone */}
            <div
              {...getRootProps()}
              className={`
                glass-strong rounded-2xl p-12 text-center cursor-pointer
                transition-all duration-300 border-2 border-dashed
                ${isDragActive 
                  ? 'border-primary-400 bg-primary-500/10' 
                  : 'border-white/20 hover:border-primary-500/50 hover:bg-white/5'
                }
                ${selectedFile ? 'border-primary-500 bg-primary-500/5' : ''}
              `}
            >
              <input {...getInputProps()} />
              
              {!selectedFile ? (
                <>
                  <Upload className="w-16 h-16 mx-auto mb-4 text-primary-400" />
                  <h3 className="text-2xl font-bold text-white mb-2">
                    {isDragActive ? 'Drop your video here' : 'Upload Your Kick Video'}
                  </h3>
                  <p className="text-white/60 mb-4">
                    Drag & drop or click to select
                  </p>
                  <p className="text-sm text-white/40">
                    Supports MP4, MOV, AVI, MKV, WebM
                  </p>
                </>
              ) : (
                <>
                  <CheckCircle className="w-16 h-16 mx-auto mb-4 text-primary-400" />
                  <h3 className="text-2xl font-bold text-white mb-2">
                    {selectedFile.name}
                  </h3>
                  <p className="text-white/60">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                  <p className="text-sm text-white/40 mt-4">
                    Click to change video
                  </p>
                </>
              )}
            </div>

            {/* Analyze Button */}
            {selectedFile && (
              <motion.button
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={handleAnalyze}
                className="w-full py-4 px-8 bg-gradient-to-r from-primary-500 to-primary-600 
                         hover:from-primary-600 hover:to-primary-700 text-white font-bold 
                         rounded-xl transition-all transform hover:scale-[1.02] 
                         shadow-lg shadow-primary-500/50"
              >
                <div className="flex items-center justify-center space-x-2">
                  <Film className="w-5 h-5" />
                  <span>Analyze Kick</span>
                </div>
              </motion.button>
            )}

            {/* Error */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="flex items-center space-x-2 p-4 bg-red-500/10 border border-red-500/30 rounded-xl"
              >
                <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
                <p className="text-red-300">{error}</p>
              </motion.div>
            )}
          </motion.div>
        ) : (
          <motion.div
            key="analyzing"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-strong rounded-2xl p-12 text-center"
          >
            <Loader2 className="w-16 h-16 mx-auto mb-6 text-primary-400 animate-spin" />
            
            <h3 className="text-2xl font-bold text-white mb-2">
              Analyzing Your Kick
            </h3>
            
            <p className="text-white/60 mb-8">{analysisStage}</p>
            
            {/* Progress Bar */}
            <div className="w-full bg-white/10 rounded-full h-3 overflow-hidden mb-4">
              <motion.div
                className="h-full bg-gradient-to-r from-primary-400 to-primary-600"
                initial={{ width: 0 }}
                animate={{ width: `${uploadProgress}%` }}
                transition={{ duration: 0.3 }}
              />
            </div>
            
            <p className="text-white/40 text-sm">{uploadProgress}% Complete</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

