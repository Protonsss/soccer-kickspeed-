'use client'

import { motion } from 'framer-motion'
import { ArrowLeft, Download, Share2 } from 'lucide-react'
import { AnalysisData } from '@/types'
import MetricsOverview from './MetricsOverview'
import SpeedChart from './SpeedChart'
import TrajectoryVisualization from './TrajectoryVisualization'
import GoalPlacement from './GoalPlacement'
import DetailedMetrics from './DetailedMetrics'

interface AnalysisResultsProps {
  data: AnalysisData
  onNewAnalysis: () => void
}

export default function AnalysisResults({ data, onNewAnalysis }: AnalysisResultsProps) {
  const { metrics } = data

  const handleDownloadReport = () => {
    const report = JSON.stringify(data, null, 2)
    const blob = new Blob([report], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `kickspeed-analysis-${data.analysis_id}.json`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={onNewAnalysis}
          className="flex items-center space-x-2 px-4 py-2 glass rounded-lg hover:glass-strong transition-all"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>New Analysis</span>
        </button>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleDownloadReport}
            className="flex items-center space-x-2 px-4 py-2 glass rounded-lg hover:glass-strong transition-all"
          >
            <Download className="w-4 h-4" />
            <span className="hidden md:inline">Download Report</span>
          </button>
          
          <button className="flex items-center space-x-2 px-4 py-2 glass rounded-lg hover:glass-strong transition-all">
            <Share2 className="w-4 h-4" />
            <span className="hidden md:inline">Share</span>
          </button>
        </div>
      </div>

      {/* Overall Score */}
      <div className="glass-strong rounded-2xl p-8 text-center">
        <h2 className="text-2xl font-bold text-white/60 mb-4">Overall Score</h2>
        <div className="relative inline-block">
          <svg className="w-48 h-48" viewBox="0 0 200 200">
            <circle
              cx="100"
              cy="100"
              r="90"
              fill="none"
              stroke="rgba(255,255,255,0.1)"
              strokeWidth="12"
            />
            <motion.circle
              cx="100"
              cy="100"
              r="90"
              fill="none"
              stroke="url(#gradient)"
              strokeWidth="12"
              strokeLinecap="round"
              strokeDasharray={`${2 * Math.PI * 90}`}
              initial={{ strokeDashoffset: 2 * Math.PI * 90 }}
              animate={{ 
                strokeDashoffset: 2 * Math.PI * 90 * (1 - metrics.overall_score / 100) 
              }}
              transition={{ duration: 1.5, ease: "easeOut" }}
              transform="rotate(-90 100 100)"
            />
            <defs>
              <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#4ade80" />
                <stop offset="100%" stopColor="#22c55e" />
              </linearGradient>
            </defs>
          </svg>
          <div className="absolute inset-0 flex items-center justify-center">
            <div>
              <div className="text-6xl font-bold text-white">
                {Math.round(metrics.overall_score)}
              </div>
              <div className="text-white/60">/ 100</div>
            </div>
          </div>
        </div>
        
        <div className="mt-4">
          <div className={`inline-block px-4 py-2 rounded-full ${
            metrics.overall_score >= 80 ? 'bg-green-500/20 text-green-300' :
            metrics.overall_score >= 60 ? 'bg-yellow-500/20 text-yellow-300' :
            'bg-red-500/20 text-red-300'
          }`}>
            {metrics.overall_score >= 80 ? '🔥 Excellent' :
             metrics.overall_score >= 60 ? '⚡ Good' :
             '💪 Keep Training'}
          </div>
        </div>
      </div>

      {/* Metrics Overview Cards */}
      <MetricsOverview metrics={metrics} />

      {/* Speed Chart */}
      <SpeedChart data={data} />

      {/* Trajectory Visualization */}
      <TrajectoryVisualization data={data} />

      {/* Goal Placement Heat Map */}
      <GoalPlacement metrics={metrics.placement} />

      {/* Detailed Metrics */}
      <DetailedMetrics metrics={metrics} videoInfo={data.video_info} />
    </motion.div>
  )
}

