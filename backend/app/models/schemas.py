from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class VideoInfo(BaseModel):
    width: int
    height: int
    fps: float
    total_frames: int
    duration: float


class BallPosition(BaseModel):
    frame: int
    timestamp: float
    x: float
    y: float
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]


class TrackingData(BaseModel):
    positions: List[BallPosition]
    total_tracked_frames: int
    tracking_quality: float


class SpeedMetrics(BaseModel):
    max_speed_kmh: float
    max_speed_mph: float
    avg_speed_kmh: float
    avg_speed_mph: float
    initial_speed_kmh: float
    speed_at_goal_kmh: Optional[float] = None


class TrajectoryMetrics(BaseModel):
    launch_angle_deg: float
    max_height_meters: float
    distance_traveled_meters: float
    arc_type: str  # "ground", "low", "medium", "high"
    trajectory_smoothness: float


class SpinMetrics(BaseModel):
    spin_rate_rpm: Optional[float] = None
    spin_axis: Optional[str] = None  # "topspin", "backspin", "sidespin_left", "sidespin_right"
    spin_efficiency: Optional[float] = None
    estimated: bool = True


class PlacementMetrics(BaseModel):
    target_zone: str  # "top_left", "top_right", "center", "bottom_left", "bottom_right", "wide_left", "wide_right", "over"
    goal_reached: bool
    distance_from_center_x: float  # meters from goal center
    distance_from_center_y: float  # meters from goal center
    accuracy_score: float  # 0-100


class PowerMetrics(BaseModel):
    estimated_foot_speed_kmh: float
    impact_power_joules: Optional[float] = None
    strike_quality: str  # "perfect", "good", "average", "poor"
    contact_type: str  # "instep", "outside", "toe", "laces", "inside"


class TimingMetrics(BaseModel):
    kick_frame: int
    kick_time: float
    flight_time_seconds: float
    time_to_goal: Optional[float] = None


class ComprehensiveMetrics(BaseModel):
    speed: SpeedMetrics
    trajectory: TrajectoryMetrics
    spin: SpinMetrics
    placement: PlacementMetrics
    power: PowerMetrics
    timing: TimingMetrics
    overall_score: float  # 0-100, composite score
    

class CalibrationData(BaseModel):
    method: str  # "goal", "manual", "reference_object"
    pixels_per_meter: float
    confidence: float
    reference_points: Optional[List[List[float]]] = None


class AnalysisResponse(BaseModel):
    analysis_id: str
    timestamp: datetime
    video_info: VideoInfo
    ball_tracking: Dict[str, Any]
    metrics: ComprehensiveMetrics
    calibration: Optional[CalibrationData] = None
    success: bool
    message: str
    warnings: Optional[List[str]] = None


class AnalysisHistory(BaseModel):
    analyses: List[AnalysisResponse]
    total_kicks: int
    best_speed: float
    average_speed: float
    improvement_trend: float


class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None

