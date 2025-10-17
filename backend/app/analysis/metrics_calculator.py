import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from scipy.interpolate import interp1d
from scipy.signal import savgol_filter
import cv2
import asyncio
from concurrent.futures import ThreadPoolExecutor

from app.models.schemas import (
    ComprehensiveMetrics, SpeedMetrics, TrajectoryMetrics,
    SpinMetrics, PlacementMetrics, PowerMetrics, TimingMetrics
)
from app.core.config import settings


class MetricsCalculator:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=2)
        self.goal_width_m = settings.GOAL_WIDTH_METERS
        self.goal_height_m = settings.GOAL_HEIGHT_METERS
        self.ball_diameter_cm = settings.BALL_DIAMETER_CM
        self.ball_mass_kg = 0.43  # Standard soccer ball mass
    
    async def calculate_all_metrics(
        self,
        tracking_data: Dict[str, Any],
        video_info: Dict[str, Any],
        reference_distance: Optional[float] = None,
        use_goal_calibration: bool = True
    ) -> ComprehensiveMetrics:
        """Calculate all metrics from tracking data"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor,
            self._calculate_all_metrics_sync,
            tracking_data,
            video_info,
            reference_distance,
            use_goal_calibration
        )
    
    def _calculate_all_metrics_sync(
        self,
        tracking_data: Dict[str, Any],
        video_info: Dict[str, Any],
        reference_distance: Optional[float],
        use_goal_calibration: bool
    ) -> ComprehensiveMetrics:
        """Synchronous metrics calculation"""
        
        positions = tracking_data['positions']
        fps = video_info['fps']
        
        # Calculate calibration
        pixels_per_meter = self._calculate_calibration(
            positions, video_info, reference_distance, use_goal_calibration
        )
        
        # Extract trajectories
        times = np.array([p['timestamp'] for p in positions])
        x_pixels = np.array([p['x'] for p in positions])
        y_pixels = np.array([p['y'] for p in positions])
        
        # Convert to meters
        x_meters = x_pixels / pixels_per_meter
        y_meters = y_pixels / pixels_per_meter
        
        # Smooth trajectories using Savitzky-Golay filter
        if len(positions) > 5:
            window = min(11, len(positions) if len(positions) % 2 == 1 else len(positions) - 1)
            x_meters = savgol_filter(x_meters, window, 3)
            y_meters = savgol_filter(y_meters, window, 3)
        
        # Calculate metrics
        speed_metrics = self._calculate_speed_metrics(times, x_meters, y_meters, fps)
        trajectory_metrics = self._calculate_trajectory_metrics(times, x_meters, y_meters, positions)
        spin_metrics = self._calculate_spin_metrics(positions, speed_metrics, fps)
        placement_metrics = self._calculate_placement_metrics(x_meters, y_meters, video_info, pixels_per_meter)
        power_metrics = self._calculate_power_metrics(speed_metrics, trajectory_metrics)
        timing_metrics = self._calculate_timing_metrics(positions, fps, times)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(
            speed_metrics, trajectory_metrics, placement_metrics, power_metrics
        )
        
        return ComprehensiveMetrics(
            speed=speed_metrics,
            trajectory=trajectory_metrics,
            spin=spin_metrics,
            placement=placement_metrics,
            power=power_metrics,
            timing=timing_metrics,
            overall_score=overall_score
        )
    
    def _calculate_calibration(
        self,
        positions: List[Dict],
        video_info: Dict[str, Any],
        reference_distance: Optional[float],
        use_goal_calibration: bool
    ) -> float:
        """Calculate pixels per meter for calibration"""
        
        if reference_distance:
            # Use manual reference distance
            # Assume ball travels approximately reference_distance meters
            total_pixels = np.sqrt(
                (positions[-1]['x'] - positions[0]['x'])**2 +
                (positions[-1]['y'] - positions[0]['y'])**2
            )
            return total_pixels / reference_distance
        
        # Default calibration based on typical soccer ball size and distance
        # Assume camera is ~10-15 meters from the action
        # Standard ball is ~22cm diameter
        
        # Get average ball size in pixels
        avg_ball_size = np.mean([
            p['bbox'][2] - p['bbox'][0] for p in positions
        ])
        
        # Typical ball appears ~20-40 pixels at 10-15 meters
        # This is a rough estimate: pixels_per_meter = (avg_ball_size / ball_diameter_in_meters)
        ball_diameter_m = self.ball_diameter_cm / 100.0
        pixels_per_meter = avg_ball_size / ball_diameter_m
        
        # Clamp to reasonable values
        pixels_per_meter = np.clip(pixels_per_meter, 10, 500)
        
        return float(pixels_per_meter)
    
    def _calculate_speed_metrics(
        self,
        times: np.ndarray,
        x_meters: np.ndarray,
        y_meters: np.ndarray,
        fps: float
    ) -> SpeedMetrics:
        """Calculate speed metrics"""
        
        # Calculate velocities
        dt = np.diff(times)
        dx = np.diff(x_meters)
        dy = np.diff(y_meters)
        
        # Speed in m/s
        speeds_ms = np.sqrt(dx**2 + dy**2) / dt
        
        # Convert to km/h and mph
        speeds_kmh = speeds_ms * 3.6
        speeds_mph = speeds_ms * 2.23694
        
        # Handle edge cases
        if len(speeds_kmh) == 0:
            speeds_kmh = np.array([0])
            speeds_mph = np.array([0])
        
        max_speed_kmh = float(np.max(speeds_kmh))
        max_speed_mph = float(np.max(speeds_mph))
        avg_speed_kmh = float(np.mean(speeds_kmh))
        avg_speed_mph = float(np.mean(speeds_mph))
        
        # Initial speed (first few frames)
        initial_speed_kmh = float(np.mean(speeds_kmh[:3])) if len(speeds_kmh) >= 3 else float(speeds_kmh[0])
        
        # Speed at goal (last few frames)
        speed_at_goal_kmh = float(np.mean(speeds_kmh[-3:])) if len(speeds_kmh) >= 3 else float(speeds_kmh[-1])
        
        return SpeedMetrics(
            max_speed_kmh=max_speed_kmh,
            max_speed_mph=max_speed_mph,
            avg_speed_kmh=avg_speed_kmh,
            avg_speed_mph=avg_speed_mph,
            initial_speed_kmh=initial_speed_kmh,
            speed_at_goal_kmh=speed_at_goal_kmh
        )
    
    def _calculate_trajectory_metrics(
        self,
        times: np.ndarray,
        x_meters: np.ndarray,
        y_meters: np.ndarray,
        positions: List[Dict]
    ) -> TrajectoryMetrics:
        """Calculate trajectory metrics"""
        
        # Launch angle (angle at start of trajectory)
        if len(x_meters) >= 3:
            dx = x_meters[2] - x_meters[0]
            dy = y_meters[2] - y_meters[0]
            launch_angle_rad = np.arctan2(-dy, dx)  # Negative because y increases downward
            launch_angle_deg = float(np.degrees(launch_angle_rad))
        else:
            launch_angle_deg = 0.0
        
        # Max height (minimum y value, since y=0 is top of frame)
        max_height_idx = np.argmin(y_meters)
        max_height_meters = float(np.abs(y_meters[max_height_idx] - y_meters[0]))
        
        # Distance traveled
        distance_traveled_meters = float(np.sqrt(
            (x_meters[-1] - x_meters[0])**2 +
            (y_meters[-1] - y_meters[0])**2
        ))
        
        # Determine arc type
        if max_height_meters < 0.5:
            arc_type = "ground"
        elif max_height_meters < 1.5:
            arc_type = "low"
        elif max_height_meters < 3.0:
            arc_type = "medium"
        else:
            arc_type = "high"
        
        # Trajectory smoothness (inverse of curvature variation)
        if len(x_meters) > 3:
            # Calculate curvature at each point
            dx_dt = np.gradient(x_meters)
            dy_dt = np.gradient(y_meters)
            d2x_dt2 = np.gradient(dx_dt)
            d2y_dt2 = np.gradient(dy_dt)
            
            curvature = np.abs(dx_dt * d2y_dt2 - dy_dt * d2x_dt2) / (dx_dt**2 + dy_dt**2)**1.5
            smoothness = float(1.0 / (1.0 + np.std(curvature)))
        else:
            smoothness = 1.0
        
        return TrajectoryMetrics(
            launch_angle_deg=launch_angle_deg,
            max_height_meters=max_height_meters,
            distance_traveled_meters=distance_traveled_meters,
            arc_type=arc_type,
            trajectory_smoothness=smoothness
        )
    
    def _calculate_spin_metrics(
        self,
        positions: List[Dict],
        speed_metrics: SpeedMetrics,
        fps: float
    ) -> SpinMetrics:
        """Estimate spin metrics"""
        
        # Spin estimation is complex and requires high-speed footage
        # We'll provide rough estimates based on trajectory curvature
        
        # For now, return estimated values
        # In a real implementation, this would use:
        # - Ball rotation detection via pattern matching
        # - Magnus effect analysis
        # - Trajectory deviation from parabolic path
        
        spin_rate_rpm = None
        spin_axis = None
        spin_efficiency = None
        
        # Rough estimation: if ball curves significantly, there's spin
        if len(positions) > 10:
            # Analyze horizontal movement pattern
            x_positions = [p['x'] for p in positions]
            x_curve = np.polyfit(range(len(x_positions)), x_positions, 2)[0]
            
            if abs(x_curve) > 0.1:
                spin_rate_rpm = abs(x_curve) * 500  # Very rough estimate
                spin_axis = "sidespin_right" if x_curve > 0 else "sidespin_left"
                spin_efficiency = 0.6
        
        return SpinMetrics(
            spin_rate_rpm=spin_rate_rpm,
            spin_axis=spin_axis,
            spin_efficiency=spin_efficiency,
            estimated=True
        )
    
    def _calculate_placement_metrics(
        self,
        x_meters: np.ndarray,
        y_meters: np.ndarray,
        video_info: Dict[str, Any],
        pixels_per_meter: float
    ) -> PlacementMetrics:
        """Calculate shot placement metrics"""
        
        # Final position
        final_x = x_meters[-1]
        final_y = y_meters[-1]
        
        # Assume goal is at the end of trajectory
        # Center of frame is approximately goal center
        frame_center_x = (video_info['width'] / 2) / pixels_per_meter
        frame_center_y = (video_info['height'] / 2) / pixels_per_meter
        
        # Distance from center
        dist_from_center_x = final_x - frame_center_x
        dist_from_center_y = final_y - frame_center_y
        
        # Determine zone
        goal_half_width = self.goal_width_m / 2
        goal_half_height = self.goal_height_m / 2
        
        # Check if in goal
        in_goal_x = abs(dist_from_center_x) < goal_half_width
        in_goal_y = abs(dist_from_center_y) < goal_half_height
        goal_reached = in_goal_x and in_goal_y
        
        # Determine target zone
        if not in_goal_x:
            if dist_from_center_x < 0:
                target_zone = "wide_left"
            else:
                target_zone = "wide_right"
        elif not in_goal_y:
            if dist_from_center_y < 0:
                target_zone = "over"
            else:
                target_zone = "below"
        else:
            # In goal - determine quadrant
            if dist_from_center_y < -goal_half_height / 2:
                if dist_from_center_x < 0:
                    target_zone = "top_left"
                else:
                    target_zone = "top_right"
            elif dist_from_center_y > goal_half_height / 2:
                if dist_from_center_x < 0:
                    target_zone = "bottom_left"
                else:
                    target_zone = "bottom_right"
            else:
                target_zone = "center"
        
        # Accuracy score (0-100)
        # Best placement is top corners
        if goal_reached:
            # Distance from ideal spots (top corners)
            dist_to_top_left = np.sqrt(
                (dist_from_center_x + goal_half_width * 0.8)**2 +
                (dist_from_center_y + goal_half_height * 0.8)**2
            )
            dist_to_top_right = np.sqrt(
                (dist_from_center_x - goal_half_width * 0.8)**2 +
                (dist_from_center_y + goal_half_height * 0.8)**2
            )
            min_dist = min(dist_to_top_left, dist_to_top_right)
            accuracy_score = float(max(0, 100 - min_dist * 20))
        else:
            # Miss - low score based on how far off
            total_miss = np.sqrt(
                max(0, abs(dist_from_center_x) - goal_half_width)**2 +
                max(0, abs(dist_from_center_y) - goal_half_height)**2
            )
            accuracy_score = float(max(0, 40 - total_miss * 10))
        
        return PlacementMetrics(
            target_zone=target_zone,
            goal_reached=goal_reached,
            distance_from_center_x=float(dist_from_center_x),
            distance_from_center_y=float(dist_from_center_y),
            accuracy_score=accuracy_score
        )
    
    def _calculate_power_metrics(
        self,
        speed_metrics: SpeedMetrics,
        trajectory_metrics: TrajectoryMetrics
    ) -> PowerMetrics:
        """Calculate power metrics"""
        
        # Estimate foot speed (typically 20-30% faster than ball speed)
        estimated_foot_speed_kmh = speed_metrics.max_speed_kmh * 1.25
        
        # Calculate kinetic energy (power)
        ball_speed_ms = speed_metrics.max_speed_kmh / 3.6
        impact_power_joules = 0.5 * self.ball_mass_kg * (ball_speed_ms ** 2)
        
        # Determine strike quality based on speed and trajectory
        if speed_metrics.max_speed_kmh > 100:
            strike_quality = "perfect"
        elif speed_metrics.max_speed_kmh > 80:
            strike_quality = "good"
        elif speed_metrics.max_speed_kmh > 60:
            strike_quality = "average"
        else:
            strike_quality = "poor"
        
        # Estimate contact type based on trajectory
        if trajectory_metrics.arc_type == "ground":
            contact_type = "toe"
        elif trajectory_metrics.launch_angle_deg > 30:
            contact_type = "instep"
        elif trajectory_metrics.launch_angle_deg < 10:
            contact_type = "laces"
        else:
            contact_type = "inside"
        
        return PowerMetrics(
            estimated_foot_speed_kmh=estimated_foot_speed_kmh,
            impact_power_joules=impact_power_joules,
            strike_quality=strike_quality,
            contact_type=contact_type
        )
    
    def _calculate_timing_metrics(
        self,
        positions: List[Dict],
        fps: float,
        times: np.ndarray
    ) -> TimingMetrics:
        """Calculate timing metrics"""
        
        # Kick frame (first frame)
        kick_frame = positions[0]['frame']
        kick_time = positions[0]['timestamp']
        
        # Flight time
        flight_time_seconds = positions[-1]['timestamp'] - kick_time
        
        # Time to goal (same as flight time for now)
        time_to_goal = flight_time_seconds
        
        return TimingMetrics(
            kick_frame=kick_frame,
            kick_time=kick_time,
            flight_time_seconds=flight_time_seconds,
            time_to_goal=time_to_goal
        )
    
    def _calculate_overall_score(
        self,
        speed_metrics: SpeedMetrics,
        trajectory_metrics: TrajectoryMetrics,
        placement_metrics: PlacementMetrics,
        power_metrics: PowerMetrics
    ) -> float:
        """Calculate overall composite score (0-100)"""
        
        # Speed score (max 100 km/h = 100 points)
        speed_score = min(100, speed_metrics.max_speed_kmh)
        
        # Trajectory score (smooth, appropriate arc)
        trajectory_score = trajectory_metrics.trajectory_smoothness * 100
        
        # Placement score (already 0-100)
        placement_score = placement_metrics.accuracy_score
        
        # Power score (strike quality)
        power_score_map = {
            "perfect": 100,
            "good": 80,
            "average": 60,
            "poor": 40
        }
        power_score = power_score_map.get(power_metrics.strike_quality, 50)
        
        # Weighted average
        overall = (
            speed_score * 0.35 +
            placement_score * 0.35 +
            power_score * 0.15 +
            trajectory_score * 0.15
        )
        
        return float(overall)

