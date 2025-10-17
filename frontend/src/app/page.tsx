'use client'

import { useState } from 'react'
import VideoUploader from '@/components/VideoUploader'
import AnalysisResults from '@/components/AnalysisResults'
import Header from '@/components/Header'
import Hero from '@/components/Hero'
import { AnalysisData } from '@/types'

export default function Home() {
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  const handleAnalysisComplete = (data: AnalysisData) => {
    setAnalysisData(data)
    setIsAnalyzing(false)
  }

  const handleNewAnalysis = () => {
    setAnalysisData(null)
  }

  return (
    <main className="min-h-screen">
      <Header />
      
      {!analysisData && !isAnalyzing && <Hero />}
      
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        {!analysisData ? (
          <VideoUploader 
            onAnalysisComplete={handleAnalysisComplete}
            isAnalyzing={isAnalyzing}
            setIsAnalyzing={setIsAnalyzing}
          />
        ) : (
          <AnalysisResults 
            data={analysisData}
            onNewAnalysis={handleNewAnalysis}
          />
        )}
      </div>

      {/* Footer */}
      <footer className="mt-20 py-8 border-t border-white/10">
        <div className="container mx-auto px-4 text-center text-white/60">
          <p>KickSpeed Pro © 2025 - Ultra-Accurate Soccer Kick Analysis</p>
          <p className="text-sm mt-2">Powered by YOLOv8, PyTorch & Advanced Computer Vision</p>
        </div>
      </footer>
    </main>
  )
}

