'use client'

import { motion } from 'framer-motion'
import { Gauge, Target, TrendingUp, Zap, Wind, Clock } from 'lucide-react'
import { ComprehensiveMetrics } from '@/types'

interface MetricsOverviewProps {
  metrics: ComprehensiveMetrics
}

export default function MetricsOverview({ metrics }: MetricsOverviewProps) {
  const cards = [
    {
      icon: Gauge,
      label: 'Max Speed',
      value: `${metrics.speed.max_speed_kmh.toFixed(1)} km/h`,
      subValue: `${metrics.speed.max_speed_mph.toFixed(1)} mph`,
      color: 'from-red-500 to-orange-500',
      iconBg: 'bg-red-500/20',
      iconColor: 'text-red-400'
    },
    {
      icon: Target,
      label: 'Accuracy',
      value: `${metrics.placement.accuracy_score.toFixed(0)}%`,
      subValue: metrics.placement.target_zone.replace('_', ' '),
      color: 'from-blue-500 to-cyan-500',
      iconBg: 'bg-blue-500/20',
      iconColor: 'text-blue-400'
    },
    {
      icon: TrendingUp,
      label: 'Launch Angle',
      value: `${metrics.trajectory.launch_angle_deg.toFixed(1)}°`,
      subValue: metrics.trajectory.arc_type,
      color: 'from-purple-500 to-pink-500',
      iconBg: 'bg-purple-500/20',
      iconColor: 'text-purple-400'
    },
    {
      icon: Zap,
      label: 'Strike Power',
      value: metrics.power.strike_quality,
      subValue: metrics.power.contact_type,
      color: 'from-yellow-500 to-orange-500',
      iconBg: 'bg-yellow-500/20',
      iconColor: 'text-yellow-400'
    },
    {
      icon: Wind,
      label: 'Spin Rate',
      value: metrics.spin.spin_rate_rpm ? `${metrics.spin.spin_rate_rpm.toFixed(0)} rpm` : 'N/A',
      subValue: metrics.spin.spin_axis || 'No spin detected',
      color: 'from-green-500 to-emerald-500',
      iconBg: 'bg-green-500/20',
      iconColor: 'text-green-400'
    },
    {
      icon: Clock,
      label: 'Flight Time',
      value: `${metrics.timing.flight_time_seconds.toFixed(2)}s`,
      subValue: `${metrics.trajectory.distance_traveled_meters.toFixed(1)}m traveled`,
      color: 'from-indigo-500 to-blue-500',
      iconBg: 'bg-indigo-500/20',
      iconColor: 'text-indigo-400'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {cards.map((card, idx) => (
        <motion.div
          key={card.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: idx * 0.1 }}
          className="glass-strong rounded-xl p-6 hover:scale-[1.02] transition-transform"
        >
          <div className="flex items-start justify-between mb-4">
            <div className={`${card.iconBg} p-3 rounded-lg`}>
              <card.icon className={`w-6 h-6 ${card.iconColor}`} />
            </div>
          </div>
          
          <h3 className="text-white/60 text-sm font-medium mb-2">{card.label}</h3>
          <div className={`text-3xl font-bold bg-gradient-to-r ${card.color} bg-clip-text text-transparent mb-1`}>
            {card.value}
          </div>
          <p className="text-white/40 text-sm capitalize">{card.subValue}</p>
        </motion.div>
      ))}
    </div>
  )
}

