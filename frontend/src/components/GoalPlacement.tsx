'use client'

import { motion } from 'framer-motion'
import { PlacementMetrics } from '@/types'

interface GoalPlacementProps {
  metrics: PlacementMetrics
}

export default function GoalPlacement({ metrics }: GoalPlacementProps) {
  // Normalize position to 0-100 range for visualization
  const normalizedX = 50 + (metrics.distance_from_center_x / 7.32) * 100
  const normalizedY = 50 + (metrics.distance_from_center_y / 2.44) * 100

  // Clamp values
  const visualX = Math.max(0, Math.min(100, normalizedX))
  const visualY = Math.max(0, Math.min(100, normalizedY))

  const getZoneColor = (zone: string) => {
    const colors: { [key: string]: string } = {
      'top_left': 'text-green-400',
      'top_right': 'text-green-400',
      'top_center': 'text-green-400',
      'center': 'text-yellow-400',
      'bottom_left': 'text-blue-400',
      'bottom_right': 'text-blue-400',
      'wide_left': 'text-red-400',
      'wide_right': 'text-red-400',
      'over': 'text-red-400'
    }
    return colors[zone] || 'text-white'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.4 }}
      className="glass-strong rounded-2xl p-6"
    >
      <h3 className="text-2xl font-bold text-white mb-6">Shot Placement</h3>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Goal Visualization */}
        <div>
          <div className="aspect-[3/2] relative border-4 border-white/30 rounded-lg bg-gradient-to-b from-white/5 to-white/10 overflow-hidden">
            {/* Goal Grid */}
            <div className="absolute inset-0 grid grid-cols-3 grid-rows-3">
              {['top_left', 'top_center', 'top_right',
                'center_left', 'center', 'center_right',
                'bottom_left', 'bottom_center', 'bottom_right'].map((zone, idx) => (
                <div
                  key={zone}
                  className={`border border-white/10 ${
                    zone.includes('top') ? 'bg-green-500/5' : ''
                  }`}
                />
              ))}
            </div>

            {/* Heat zones overlay */}
            <div className="absolute inset-0">
              {/* Top corners (ideal zones) */}
              <div className="absolute top-0 left-0 w-1/3 h-1/3 bg-gradient-radial from-green-500/20 to-transparent" />
              <div className="absolute top-0 right-0 w-1/3 h-1/3 bg-gradient-radial from-green-500/20 to-transparent" />
            </div>

            {/* Ball impact point */}
            {metrics.goal_reached && (
              <motion.div
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: 0.5, type: "spring" }}
                className="absolute w-6 h-6 -ml-3 -mt-3"
                style={{
                  left: `${visualX}%`,
                  top: `${visualY}%`
                }}
              >
                <div className="absolute inset-0 rounded-full bg-primary-400 animate-ping" />
                <div className="absolute inset-0 rounded-full bg-primary-500 border-2 border-white" />
              </motion.div>
            )}

            {/* Goal posts */}
            <div className="absolute top-0 left-0 bottom-0 w-2 bg-white/50 rounded-l-lg" />
            <div className="absolute top-0 right-0 bottom-0 w-2 bg-white/50 rounded-r-lg" />
            <div className="absolute top-0 left-0 right-0 h-2 bg-white/50 rounded-t-lg" />
          </div>

          <div className="mt-4 grid grid-cols-3 gap-2">
            <div className="text-center p-2 glass rounded">
              <div className="text-xs text-white/60">Ideal Zone</div>
              <div className="w-3 h-3 mx-auto mt-1 rounded-full bg-green-500" />
            </div>
            <div className="text-center p-2 glass rounded">
              <div className="text-xs text-white/60">Good Zone</div>
              <div className="w-3 h-3 mx-auto mt-1 rounded-full bg-blue-500" />
            </div>
            <div className="text-center p-2 glass rounded">
              <div className="text-xs text-white/60">Risky Zone</div>
              <div className="w-3 h-3 mx-auto mt-1 rounded-full bg-yellow-500" />
            </div>
          </div>
        </div>

        {/* Metrics */}
        <div className="space-y-4">
          <div className="glass p-4 rounded-xl">
            <div className="text-white/60 text-sm mb-2">Target Zone</div>
            <div className={`text-2xl font-bold ${getZoneColor(metrics.target_zone)} capitalize`}>
              {metrics.target_zone.replace('_', ' ')}
            </div>
          </div>

          <div className="glass p-4 rounded-xl">
            <div className="text-white/60 text-sm mb-2">Accuracy Score</div>
            <div className="flex items-end space-x-2">
              <div className="text-3xl font-bold text-white">
                {metrics.accuracy_score.toFixed(0)}
              </div>
              <div className="text-white/60 mb-1">/ 100</div>
            </div>
            <div className="mt-2 w-full bg-white/10 rounded-full h-2 overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${metrics.accuracy_score}%` }}
                transition={{ duration: 1, delay: 0.5 }}
                className={`h-full rounded-full ${
                  metrics.accuracy_score >= 80 ? 'bg-green-500' :
                  metrics.accuracy_score >= 60 ? 'bg-yellow-500' :
                  'bg-red-500'
                }`}
              />
            </div>
          </div>

          <div className="glass p-4 rounded-xl">
            <div className="text-white/60 text-sm mb-2">Goal Status</div>
            <div className="flex items-center space-x-2">
              {metrics.goal_reached ? (
                <>
                  <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
                  <span className="text-green-400 font-semibold">GOAL! ⚽</span>
                </>
              ) : (
                <>
                  <div className="w-3 h-3 rounded-full bg-red-500" />
                  <span className="text-red-400 font-semibold">Missed</span>
                </>
              )}
            </div>
          </div>

          <div className="glass p-4 rounded-xl">
            <div className="text-white/60 text-sm mb-2">Distance from Center</div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <div className="text-xs text-white/40">Horizontal</div>
                <div className="text-lg font-bold text-white">
                  {Math.abs(metrics.distance_from_center_x).toFixed(2)}m
                  <span className="text-sm text-white/60 ml-1">
                    {metrics.distance_from_center_x > 0 ? '→' : '←'}
                  </span>
                </div>
              </div>
              <div>
                <div className="text-xs text-white/40">Vertical</div>
                <div className="text-lg font-bold text-white">
                  {Math.abs(metrics.distance_from_center_y).toFixed(2)}m
                  <span className="text-sm text-white/60 ml-1">
                    {metrics.distance_from_center_y > 0 ? '↓' : '↑'}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

