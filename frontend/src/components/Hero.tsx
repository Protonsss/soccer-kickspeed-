'use client'

import { motion } from 'framer-motion'
import { Zap, Target, TrendingUp, Wind } from 'lucide-react'

export default function Hero() {
  const features = [
    { icon: Zap, label: 'Speed Analysis', desc: 'km/h & mph' },
    { icon: Target, label: 'Shot Placement', desc: 'Precision mapping' },
    { icon: TrendingUp, label: 'Trajectory', desc: 'Full arc analysis' },
    { icon: Wind, label: 'Spin Detection', desc: 'RPM & axis' },
  ]

  return (
    <div className="pt-24 pb-12">
      <div className="container mx-auto px-4 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h2 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-primary-400 via-primary-500 to-primary-600 bg-clip-text text-transparent">
            Professional Soccer
            <br />
            Kick Analysis
          </h2>
          
          <p className="text-xl md:text-2xl text-white/70 mb-12 max-w-3xl mx-auto">
            Advanced AI-powered analysis with <span className="text-primary-400 font-semibold">99% accuracy</span>.
            Upload your video and get comprehensive insights in seconds.
          </p>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto mb-12">
            {features.map((feature, idx) => (
              <motion.div
                key={feature.label}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: idx * 0.1 }}
                className="glass p-6 rounded-xl hover:glass-strong transition-all group"
              >
                <feature.icon className="w-8 h-8 mx-auto mb-3 text-primary-400 group-hover:scale-110 transition-transform" />
                <h3 className="font-semibold text-white mb-1">{feature.label}</h3>
                <p className="text-sm text-white/60">{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

