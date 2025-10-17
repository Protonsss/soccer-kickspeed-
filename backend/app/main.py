from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from pathlib import Path
from typing import Optional
import aiofiles
import uuid
from datetime import datetime

from app.core.config import settings
from app.analysis.video_processor import VideoProcessor
from app.analysis.ball_tracker import BallTracker
from app.analysis.metrics_calculator import MetricsCalculator
from app.database.database import engine, Base
from app.models import schemas

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KickSpeed Pro API",
    description="Ultra-accurate soccer kick analysis with advanced computer vision",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize processors
video_processor = VideoProcessor()
ball_tracker = BallTracker()
metrics_calculator = MetricsCalculator()

# Ensure upload directory exists
UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
async def root():
    return {
        "message": "KickSpeed Pro API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/api/analyze", response_model=schemas.AnalysisResponse)
async def analyze_kick(
    video: UploadFile = File(...),
    reference_distance: Optional[float] = None,
    use_goal_calibration: bool = True
):
    """
    Analyze a soccer kick video and return comprehensive metrics.
    
    Parameters:
    - video: Video file of the kick
    - reference_distance: Optional manual distance from camera to ball (in meters)
    - use_goal_calibration: Use goal posts for automatic calibration (default: True)
    """
    
    # Validate file
    if not video.content_type.startswith('video/'):
        raise HTTPException(status_code=400, detail="File must be a video")
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = Path(video.filename).suffix
    file_path = UPLOAD_DIR / f"{file_id}{file_extension}"
    
    try:
        # Save uploaded file
        async with aiofiles.open(file_path, 'wb') as out_file:
            content = await video.read()
            await out_file.write(content)
        
        # Process video
        print(f"Processing video: {file_path}")
        video_info = await video_processor.extract_video_info(str(file_path))
        
        # Detect and track ball
        print("Tracking ball...")
        tracking_data = await ball_tracker.track_ball(
            str(file_path),
            video_info
        )
        
        if not tracking_data or len(tracking_data['positions']) < 5:
            raise HTTPException(
                status_code=400,
                detail="Could not track ball reliably. Ensure ball is clearly visible."
            )
        
        # Calculate metrics
        print("Calculating metrics...")
        metrics = await metrics_calculator.calculate_all_metrics(
            tracking_data=tracking_data,
            video_info=video_info,
            reference_distance=reference_distance,
            use_goal_calibration=use_goal_calibration
        )
        
        # Prepare response
        response = schemas.AnalysisResponse(
            analysis_id=file_id,
            timestamp=datetime.utcnow(),
            video_info=video_info,
            ball_tracking=tracking_data,
            metrics=metrics,
            success=True,
            message="Analysis completed successfully"
        )
        
        return response
        
    except Exception as e:
        # Clean up file on error
        if file_path.exists():
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/api/quick-analyze")
async def quick_analyze(video: UploadFile = File(...)):
    """Quick analysis with default settings"""
    return await analyze_kick(video=video, use_goal_calibration=True)


@app.delete("/api/analysis/{analysis_id}")
async def delete_analysis(analysis_id: str):
    """Delete analysis data and video file"""
    file_pattern = UPLOAD_DIR / f"{analysis_id}.*"
    deleted = False
    
    for file_path in UPLOAD_DIR.glob(f"{analysis_id}.*"):
        file_path.unlink()
        deleted = True
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {"message": "Analysis deleted successfully"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

