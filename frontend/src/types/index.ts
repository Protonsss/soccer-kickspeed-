export interface VideoInfo {
  width: number
  height: number
  fps: number
  total_frames: number
  duration: number
}

export interface BallPosition {
  frame: number
  timestamp: number
  x: number
  y: number
  confidence: number
  bbox: [number, number, number, number]
}

export interface SpeedMetrics {
  max_speed_kmh: number
  max_speed_mph: number
  avg_speed_kmh: number
  avg_speed_mph: number
  initial_speed_kmh: number
  speed_at_goal_kmh: number | null
}

export interface TrajectoryMetrics {
  launch_angle_deg: number
  max_height_meters: number
  distance_traveled_meters: number
  arc_type: string
  trajectory_smoothness: number
}

export interface SpinMetrics {
  spin_rate_rpm: number | null
  spin_axis: string | null
  spin_efficiency: number | null
  estimated: boolean
}

export interface PlacementMetrics {
  target_zone: string
  goal_reached: boolean
  distance_from_center_x: number
  distance_from_center_y: number
  accuracy_score: number
}

export interface PowerMetrics {
  estimated_foot_speed_kmh: number
  impact_power_joules: number | null
  strike_quality: string
  contact_type: string
}

export interface TimingMetrics {
  kick_frame: number
  kick_time: number
  flight_time_seconds: number
  time_to_goal: number | null
}

export interface ComprehensiveMetrics {
  speed: SpeedMetrics
  trajectory: TrajectoryMetrics
  spin: SpinMetrics
  placement: PlacementMetrics
  power: PowerMetrics
  timing: TimingMetrics
  overall_score: number
}

export interface AnalysisData {
  analysis_id: string
  timestamp: string
  video_info: VideoInfo
  ball_tracking: {
    positions: BallPosition[]
    total_tracked_frames: number
    tracking_quality: number
  }
  metrics: ComprehensiveMetrics
  success: boolean
  message: string
  warnings?: string[]
}

