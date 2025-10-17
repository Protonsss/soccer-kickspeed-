'use client'

import { motion } from 'framer-motion'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts'
import { AnalysisData } from '@/types'

interface SpeedChartProps {
  data: AnalysisData
}

export default function SpeedChart({ data }: SpeedChartProps) {
  // Calculate speed between consecutive positions
  const positions = data.ball_tracking.positions
  const chartData = []

  for (let i = 1; i < positions.length; i++) {
    const prev = positions[i - 1]
    const curr = positions[i]
    
    const dx = curr.x - prev.x
    const dy = curr.y - prev.y
    const dt = curr.timestamp - prev.timestamp
    
    if (dt > 0) {
      // This is in pixels per second, we'd need calibration for real speed
      // For now, use a rough estimate
      const speed = Math.sqrt(dx * dx + dy * dy) / dt
      const speedKmh = speed * 0.1 // Rough conversion factor
      
      chartData.push({
        time: curr.timestamp.toFixed(2),
        speed: speedKmh,
        timestamp: curr.timestamp
      })
    }
  }

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      return (
        <div className="glass-strong p-3 rounded-lg border border-white/20">
          <p className="text-white font-semibold">{payload[0].value.toFixed(1)} km/h</p>
          <p className="text-white/60 text-sm">Time: {payload[0].payload.time}s</p>
        </div>
      )
    }
    return null
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="glass-strong rounded-2xl p-6"
    >
      <h3 className="text-2xl font-bold text-white mb-6">Speed Over Time</h3>
      
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData}>
            <defs>
              <linearGradient id="speedGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#22c55e" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#22c55e" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
            <XAxis 
              dataKey="time" 
              stroke="rgba(255,255,255,0.5)"
              label={{ value: 'Time (s)', position: 'insideBottom', offset: -5, fill: 'rgba(255,255,255,0.5)' }}
            />
            <YAxis 
              stroke="rgba(255,255,255,0.5)"
              label={{ value: 'Speed (km/h)', angle: -90, position: 'insideLeft', fill: 'rgba(255,255,255,0.5)' }}
            />
            <Tooltip content={<CustomTooltip />} />
            <Area 
              type="monotone" 
              dataKey="speed" 
              stroke="#22c55e" 
              strokeWidth={3}
              fill="url(#speedGradient)" 
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-3 gap-4 mt-6">
        <div className="text-center p-4 glass rounded-lg">
          <div className="text-white/60 text-sm mb-1">Initial Speed</div>
          <div className="text-2xl font-bold text-primary-400">
            {data.metrics.speed.initial_speed_kmh.toFixed(1)} km/h
          </div>
        </div>
        <div className="text-center p-4 glass rounded-lg">
          <div className="text-white/60 text-sm mb-1">Max Speed</div>
          <div className="text-2xl font-bold text-red-400">
            {data.metrics.speed.max_speed_kmh.toFixed(1)} km/h
          </div>
        </div>
        <div className="text-center p-4 glass rounded-lg">
          <div className="text-white/60 text-sm mb-1">Avg Speed</div>
          <div className="text-2xl font-bold text-blue-400">
            {data.metrics.speed.avg_speed_kmh.toFixed(1)} km/h
          </div>
        </div>
      </div>
    </motion.div>
  )
}

