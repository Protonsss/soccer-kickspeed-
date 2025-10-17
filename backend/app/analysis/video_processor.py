import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.models.schemas import VideoInfo


class VideoProcessor:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def extract_video_info(self, video_path: str) -> Dict[str, Any]:
        """Extract basic video information"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._extract_video_info_sync,
            video_path
        )
    
    def _extract_video_info_sync(self, video_path: str) -> Dict[str, Any]:
        """Synchronous video info extraction"""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError("Could not open video file")
        
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        cap.release()
        
        return {
            "width": width,
            "height": height,
            "fps": fps,
            "total_frames": total_frames,
            "duration": duration
        }
    
    async def extract_frames(self, video_path: str, max_frames: int = None) -> list:
        """Extract frames from video"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._extract_frames_sync,
            video_path,
            max_frames
        )
    
    def _extract_frames_sync(self, video_path: str, max_frames: int = None) -> list:
        """Synchronous frame extraction"""
        cap = cv2.VideoCapture(video_path)
        frames = []
        frame_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frames.append(frame)
            frame_count += 1
            
            if max_frames and frame_count >= max_frames:
                break
        
        cap.release()
        return frames
    
    def preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """Preprocess frame for better detection"""
        # Convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame_rgb
    
    def apply_frame_interpolation(self, frames: list, target_fps: int = 120) -> list:
        """Apply frame interpolation for higher temporal resolution"""
        # This would use optical flow or deep learning based interpolation
        # For now, we'll use basic interpolation
        interpolated = []
        
        for i in range(len(frames) - 1):
            interpolated.append(frames[i])
            # Add interpolated frame between current and next
            alpha = 0.5
            interp_frame = cv2.addWeighted(frames[i], alpha, frames[i + 1], 1 - alpha, 0)
            interpolated.append(interp_frame)
        
        interpolated.append(frames[-1])
        return interpolated

