'use client'

import { Activity } from 'lucide-react'

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 glass-strong">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-gradient-to-br from-primary-400 to-primary-600 p-2 rounded-lg">
              <Activity className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">KickSpeed Pro</h1>
              <p className="text-xs text-white/60">Ultra-Accurate Analysis</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="hidden md:flex items-center space-x-2 px-3 py-1.5 rounded-full bg-primary-500/20 border border-primary-500/30">
              <div className="w-2 h-2 rounded-full bg-primary-400 animate-pulse" />
              <span className="text-sm text-primary-300">99% Accuracy</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}

