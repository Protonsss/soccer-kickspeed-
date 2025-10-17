'use client'

import { motion } from 'framer-motion'
import { 
  Activity, Zap, Wind, Target, TrendingUp, Clock, 
  Gauge, Footprints, BarChart3 
} from 'lucide-react'
import { ComprehensiveMetrics, VideoInfo } from '@/types'

interface DetailedMetricsProps {
  metrics: ComprehensiveMetrics
  videoInfo: VideoInfo
}

export default function DetailedMetrics({ metrics, videoInfo }: DetailedMetricsProps) {
  const sections = [
    {
      title: 'Speed Analysis',
      icon: Gauge,
      color: 'text-red-400',
      metrics: [
        { label: 'Maximum Speed', value: `${metrics.speed.max_speed_kmh.toFixed(2)} km/h` },
        { label: 'Maximum Speed', value: `${metrics.speed.max_speed_mph.toFixed(2)} mph` },
        { label: 'Average Speed', value: `${metrics.speed.avg_speed_kmh.toFixed(2)} km/h` },
        { label: 'Initial Speed', value: `${metrics.speed.initial_speed_kmh.toFixed(2)} km/h` },
        { 
          label: 'Speed at Goal', 
          value: metrics.speed.speed_at_goal_kmh 
            ? `${metrics.speed.speed_at_goal_kmh.toFixed(2)} km/h` 
            : 'N/A' 
        }
      ]
    },
    {
      title: 'Trajectory',
      icon: TrendingUp,
      color: 'text-purple-400',
      metrics: [
        { label: 'Launch Angle', value: `${metrics.trajectory.launch_angle_deg.toFixed(2)}°` },
        { label: 'Max Height', value: `${metrics.trajectory.max_height_meters.toFixed(2)} m` },
        { label: 'Distance Traveled', value: `${metrics.trajectory.distance_traveled_meters.toFixed(2)} m` },
        { label: 'Arc Type', value: metrics.trajectory.arc_type },
        { label: 'Trajectory Smoothness', value: `${(metrics.trajectory.trajectory_smoothness * 100).toFixed(1)}%` }
      ]
    },
    {
      title: 'Spin Analysis',
      icon: Wind,
      color: 'text-green-400',
      metrics: [
        { 
          label: 'Spin Rate', 
          value: metrics.spin.spin_rate_rpm 
            ? `${metrics.spin.spin_rate_rpm.toFixed(0)} rpm` 
            : 'Not detected' 
        },
        { label: 'Spin Axis', value: metrics.spin.spin_axis || 'N/A' },
        { 
          label: 'Spin Efficiency', 
          value: metrics.spin.spin_efficiency 
            ? `${(metrics.spin.spin_efficiency * 100).toFixed(0)}%` 
            : 'N/A' 
        },
        { label: 'Estimated', value: metrics.spin.estimated ? 'Yes' : 'No' }
      ]
    },
    {
      title: 'Power Metrics',
      icon: Zap,
      color: 'text-yellow-400',
      metrics: [
        { label: 'Estimated Foot Speed', value: `${metrics.power.estimated_foot_speed_kmh.toFixed(2)} km/h` },
        { 
          label: 'Impact Power', 
          value: metrics.power.impact_power_joules 
            ? `${metrics.power.impact_power_joules.toFixed(2)} J` 
            : 'N/A' 
        },
        { label: 'Strike Quality', value: metrics.power.strike_quality },
        { label: 'Contact Type', value: metrics.power.contact_type }
      ]
    },
    {
      title: 'Timing',
      icon: Clock,
      color: 'text-blue-400',
      metrics: [
        { label: 'Kick Frame', value: metrics.timing.kick_frame.toString() },
        { label: 'Kick Time', value: `${metrics.timing.kick_time.toFixed(3)} s` },
        { label: 'Flight Time', value: `${metrics.timing.flight_time_seconds.toFixed(3)} s` },
        { 
          label: 'Time to Goal', 
          value: metrics.timing.time_to_goal 
            ? `${metrics.timing.time_to_goal.toFixed(3)} s` 
            : 'N/A' 
        }
      ]
    },
    {
      title: 'Video Info',
      icon: Activity,
      color: 'text-cyan-400',
      metrics: [
        { label: 'Resolution', value: `${videoInfo.width}x${videoInfo.height}` },
        { label: 'Frame Rate', value: `${videoInfo.fps.toFixed(2)} fps` },
        { label: 'Total Frames', value: videoInfo.total_frames.toString() },
        { label: 'Duration', value: `${videoInfo.duration.toFixed(2)} s` }
      ]
    }
  ]

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.5 }}
      className="glass-strong rounded-2xl p-6"
    >
      <h3 className="text-2xl font-bold text-white mb-6">Detailed Analysis</h3>

      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {sections.map((section, idx) => (
          <motion.div
            key={section.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.4, delay: 0.6 + idx * 0.1 }}
            className="glass p-5 rounded-xl"
          >
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-2 bg-white/5 rounded-lg">
                <section.icon className={`w-5 h-5 ${section.color}`} />
              </div>
              <h4 className="font-semibold text-white">{section.title}</h4>
            </div>

            <div className="space-y-3">
              {section.metrics.map((metric, metricIdx) => (
                <div key={metricIdx} className="flex justify-between items-center">
                  <span className="text-white/60 text-sm">{metric.label}</span>
                  <span className="text-white font-medium text-sm">{metric.value}</span>
                </div>
              ))}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Professional Comparison */}
      <div className="mt-6 glass p-6 rounded-xl">
        <h4 className="font-semibold text-white mb-4 flex items-center">
          <BarChart3 className="w-5 h-5 mr-2 text-primary-400" />
          Professional Comparison
        </h4>
        
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <div className="text-white/60 text-sm mb-2">Your Max Speed</div>
            <div className="text-2xl font-bold text-white mb-2">
              {metrics.speed.max_speed_kmh.toFixed(1)} km/h
            </div>
            <div className="text-xs text-white/40">
              vs Professional avg: 90-110 km/h
            </div>
          </div>

          <div>
            <div className="text-white/60 text-sm mb-2">Accuracy</div>
            <div className="text-2xl font-bold text-white mb-2">
              {metrics.placement.accuracy_score.toFixed(0)}%
            </div>
            <div className="text-xs text-white/40">
              vs Professional avg: 70-85%
            </div>
          </div>

          <div>
            <div className="text-white/60 text-sm mb-2">Strike Quality</div>
            <div className="text-2xl font-bold text-white mb-2 capitalize">
              {metrics.power.strike_quality}
            </div>
            <div className="text-xs text-white/40">
              Professional standard: Perfect/Good
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

