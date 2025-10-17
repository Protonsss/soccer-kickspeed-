from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Settings
    APP_NAME: str = "KickSpeed Pro"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./kickspeed.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Upload Settings
    MAX_FILE_SIZE: int = 100000000  # 100MB
    UPLOAD_DIR: str = "./uploads"
    
    # Model Settings
    CONFIDENCE_THRESHOLD: float = 0.5
    IOU_THRESHOLD: float = 0.45
    
    # Analysis Settings
    MIN_TRACKING_FRAMES: int = 5
    GOAL_WIDTH_METERS: float = 7.32  # Standard goal width
    GOAL_HEIGHT_METERS: float = 2.44  # Standard goal height
    BALL_DIAMETER_CM: float = 22.0  # Standard ball diameter
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

