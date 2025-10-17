'use client'

import { motion } from 'framer-motion'
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { AnalysisData } from '@/types'

interface TrajectoryVisualizationProps {
  data: AnalysisData
}

export default function TrajectoryVisualization({ data }: TrajectoryVisualizationProps) {
  const positions = data.ball_tracking.positions

  // Normalize positions for visualization
  const minX = Math.min(...positions.map(p => p.x))
  const maxX = Math.max(...positions.map(p => p.x))
  const minY = Math.min(...positions.map(p => p.y))
  const maxY = Math.max(...positions.map(p => p.y))

  const trajectoryData = positions.map((pos, idx) => ({
    x: ((pos.x - minX) / (maxX - minX)) * 100,
    y: ((pos.y - minY) / (maxY - minY)) * 100,
    frame: pos.frame,
    timestamp: pos.timestamp,
    confidence: pos.confidence,
    index: idx
  }))

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const point = payload[0].payload
      return (
        <div className="glass-strong p-3 rounded-lg border border-white/20">
          <p className="text-white font-semibold">Frame {point.frame}</p>
          <p className="text-white/60 text-sm">{point.timestamp.toFixed(3)}s</p>
          <p className="text-white/60 text-sm">Confidence: {(point.confidence * 100).toFixed(0)}%</p>
        </div>
      )
    }
    return null
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="glass-strong rounded-2xl p-6"
    >
      <h3 className="text-2xl font-bold text-white mb-6">Ball Trajectory</h3>
      
      <div className="h-96 relative">
        <ResponsiveContainer width="100%" height="100%">
          <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis 
              type="number" 
              dataKey="x" 
              name="Horizontal Position" 
              stroke="rgba(255,255,255,0.5)"
              domain={[0, 100]}
            />
            <YAxis 
              type="number" 
              dataKey="y" 
              name="Vertical Position"
              stroke="rgba(255,255,255,0.5)"
              domain={[0, 100]}
              reversed
            />
            <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
            <Scatter 
              data={trajectoryData} 
              fill="#22c55e"
              line={{ stroke: '#22c55e', strokeWidth: 2 }}
              lineType="joint"
            >
              {trajectoryData.map((entry, index) => (
                <Cell 
                  key={`cell-${index}`}
                  fill={`rgba(34, 197, 94, ${0.3 + (index / trajectoryData.length) * 0.7})`}
                />
              ))}
            </Scatter>
          </ScatterChart>
        </ResponsiveContainer>

        {/* Start and End Markers */}
        <div className="absolute top-4 left-4 flex items-center space-x-2 glass px-3 py-1.5 rounded-lg">
          <div className="w-3 h-3 rounded-full bg-green-400 animate-pulse" />
          <span className="text-sm text-white/80">Start</span>
        </div>
        <div className="absolute top-4 right-4 flex items-center space-x-2 glass px-3 py-1.5 rounded-lg">
          <div className="w-3 h-3 rounded-full bg-red-400 animate-pulse" />
          <span className="text-sm text-white/80">End</span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
        <div className="text-center p-4 glass rounded-lg">
          <div className="text-white/60 text-sm mb-1">Max Height</div>
          <div className="text-xl font-bold text-white">
            {data.metrics.trajectory.max_height_meters.toFixed(2)}m
          </div>
        </div>
        <div className="text-center p-4 glass rounded-lg">
          <div className="text-white/60 text-sm mb-1">Distance</div>
          <div className="text-xl font-bold text-white">
            {data.metrics.trajectory.distance_traveled_meters.toFixed(2)}m
          </div>
        </div>
        <div className="text-center p-4 glass rounded-lg">
          <div className="text-white/60 text-sm mb-1">Arc Type</div>
          <div className="text-xl font-bold text-white capitalize">
            {data.metrics.trajectory.arc_type}
          </div>
        </div>
        <div className="text-center p-4 glass rounded-lg">
          <div className="text-white/60 text-sm mb-1">Smoothness</div>
          <div className="text-xl font-bold text-white">
            {(data.metrics.trajectory.trajectory_smoothness * 100).toFixed(0)}%
          </div>
        </div>
      </div>
    </motion.div>
  )
}

