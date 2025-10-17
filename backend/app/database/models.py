from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, JSON
from sqlalchemy.sql import func
from app.database.database import Base


class KickAnalysis(Base):
    __tablename__ = "kick_analyses"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Video info
    video_width = Column(Integer)
    video_height = Column(Integer)
    video_fps = Column(Float)
    video_duration = Column(Float)
    
    # Speed metrics
    max_speed_kmh = Column(Float)
    max_speed_mph = Column(Float)
    avg_speed_kmh = Column(Float)
    initial_speed_kmh = Column(Float)
    
    # Trajectory metrics
    launch_angle_deg = Column(Float)
    max_height_meters = Column(Float)
    distance_traveled_meters = Column(Float)
    arc_type = Column(String)
    
    # Placement metrics
    target_zone = Column(String)
    goal_reached = Column(Boolean)
    accuracy_score = Column(Float)
    
    # Spin metrics
    spin_rate_rpm = Column(Float, nullable=True)
    spin_axis = Column(String, nullable=True)
    
    # Power metrics
    estimated_foot_speed_kmh = Column(Float)
    strike_quality = Column(String)
    contact_type = Column(String)
    
    # Timing
    flight_time_seconds = Column(Float)
    
    # Overall
    overall_score = Column(Float)
    
    # Full data JSON
    full_metrics = Column(JSON)
    tracking_data = Column(JSON)

