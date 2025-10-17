import cv2
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import asyncio
from concurrent.futures import ThreadPoolExecutor
from filterpy.kalman import KalmanFilter
from ultralytics import YOLO
import torch

from app.core.config import settings


class BallTracker:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # Initialize YOLO model (will download on first use)
        # We'll use YOLOv8 pretrained on COCO which includes sports ball class
        try:
            self.model = YOLO('yolov8n.pt')  # Nano model for speed, can use yolov8x for accuracy
            self.model.to(self.device)
        except Exception as e:
            print(f"Warning: Could not load YOLO model: {e}")
            self.model = None
        
        # Initialize Kalman Filter for smooth tracking
        self.kf = None
        
    def _init_kalman_filter(self):
        """Initialize Kalman Filter for ball tracking"""
        kf = KalmanFilter(dim_x=4, dim_z=2)
        
        # State transition matrix (constant velocity model)
        kf.F = np.array([
            [1, 0, 1, 0],  # x = x + vx
            [0, 1, 0, 1],  # y = y + vy
            [0, 0, 1, 0],  # vx = vx
            [0, 0, 0, 1]   # vy = vy
        ])
        
        # Measurement function
        kf.H = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ])
        
        # Measurement uncertainty
        kf.R *= 10
        
        # Process uncertainty
        kf.Q *= 0.01
        
        # Initial covariance
        kf.P *= 100
        
        return kf
    
    async def track_ball(self, video_path: str, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """Track soccer ball through video"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._track_ball_sync,
            video_path,
            video_info
        )
    
    def _track_ball_sync(self, video_path: str, video_info: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous ball tracking"""
        cap = cv2.VideoCapture(video_path)
        fps = video_info['fps']
        
        positions = []
        frame_number = 0
        self.kf = self._init_kalman_filter()
        
        # Track ball using YOLO + Color detection + Optical Flow
        prev_position = None
        tracking_started = False
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            timestamp = frame_number / fps
            
            # Method 1: YOLO Detection
            ball_bbox = self._detect_ball_yolo(frame)
            
            # Method 2: Color-based detection (backup)
            if ball_bbox is None:
                ball_bbox = self._detect_ball_color(frame)
            
            # Method 3: Optical flow tracking (if previous position exists)
            if ball_bbox is None and prev_position is not None:
                ball_bbox = self._track_optical_flow(frame, prev_position)
            
            if ball_bbox is not None:
                x1, y1, x2, y2, confidence = ball_bbox
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                
                # Apply Kalman filtering for smoothing
                if not tracking_started:
                    self.kf.x = np.array([center_x, center_y, 0, 0])
                    tracking_started = True
                else:
                    self.kf.predict()
                    self.kf.update(np.array([center_x, center_y]))
                    center_x, center_y = self.kf.x[0], self.kf.x[1]
                
                position = {
                    "frame": frame_number,
                    "timestamp": timestamp,
                    "x": float(center_x),
                    "y": float(center_y),
                    "confidence": float(confidence),
                    "bbox": [float(x1), float(y1), float(x2), float(y2)]
                }
                
                positions.append(position)
                prev_position = (center_x, center_y, x2 - x1)
            
            frame_number += 1
        
        cap.release()
        
        # Calculate tracking quality
        tracking_quality = self._calculate_tracking_quality(positions, frame_number)
        
        return {
            "positions": positions,
            "total_tracked_frames": len(positions),
            "tracking_quality": tracking_quality
        }
    
    def _detect_ball_yolo(self, frame: np.ndarray) -> Optional[Tuple[float, float, float, float, float]]:
        """Detect ball using YOLO"""
        if self.model is None:
            return None
        
        try:
            # Run inference
            results = self.model(frame, conf=settings.CONFIDENCE_THRESHOLD, verbose=False)
            
            # Look for sports ball (class 32 in COCO dataset)
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    # Class 32 is sports ball, class 0 is person (we skip person)
                    if cls == 32:  # Sports ball
                        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                        confidence = float(box.conf[0])
                        return (x1, y1, x2, y2, confidence)
            
        except Exception as e:
            print(f"YOLO detection error: {e}")
        
        return None
    
    def _detect_ball_color(self, frame: np.ndarray) -> Optional[Tuple[float, float, float, float, float]]:
        """Detect ball using color detection (white/black soccer ball)"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # White color range for soccer ball
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 30, 255])
        
        mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            # Find circular contours
            for contour in contours:
                area = cv2.contourArea(contour)
                if area < 50 or area > 5000:  # Filter by size
                    continue
                
                # Check circularity
                perimeter = cv2.arcLength(contour, True)
                if perimeter == 0:
                    continue
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                
                if circularity > 0.6:  # Reasonably circular
                    x, y, w, h = cv2.boundingRect(contour)
                    return (float(x), float(y), float(x + w), float(y + h), 0.7)
        
        return None
    
    def _track_optical_flow(self, frame: np.ndarray, prev_position: Tuple[float, float, float]) -> Optional[Tuple[float, float, float, float, float]]:
        """Track ball using optical flow"""
        # This is a placeholder - would implement Lucas-Kanade or Farneback optical flow
        # For now, return None to trigger re-detection
        return None
    
    def _calculate_tracking_quality(self, positions: List[Dict], total_frames: int) -> float:
        """Calculate tracking quality score (0-1)"""
        if not positions or total_frames == 0:
            return 0.0
        
        # Factors: frame coverage, confidence, smoothness
        coverage = len(positions) / total_frames
        avg_confidence = np.mean([p['confidence'] for p in positions])
        
        # Check smoothness (no sudden jumps)
        if len(positions) > 1:
            distances = []
            for i in range(1, len(positions)):
                dx = positions[i]['x'] - positions[i-1]['x']
                dy = positions[i]['y'] - positions[i-1]['y']
                dist = np.sqrt(dx**2 + dy**2)
                distances.append(dist)
            
            # Penalize large jumps
            smoothness = 1.0 - min(1.0, np.std(distances) / 100)
        else:
            smoothness = 1.0
        
        quality = (coverage * 0.5 + avg_confidence * 0.3 + smoothness * 0.2)
        return float(quality)

