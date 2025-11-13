"""
PROPRIETARY - Extended Kalman Filter with Physics-Based Motion Model
Copyright (c) 2025 Stephen Chen. All Rights Reserved.

Advanced state estimation incorporating gravity, drag, Magnus effect,
and wind resistance for professional-grade tracking accuracy.

TRADE SECRET: Proprietary filtering algorithms with adaptive noise estimation.
"""

import numpy as np
from typing import Tuple, Optional
from dataclasses import dataclass


@dataclass
class BallState:
    """Complete ball state vector"""
    # Position (meters)
    x: float
    y: float
    z: float

    # Velocity (m/s)
    vx: float
    vy: float
    vz: float

    # Angular velocity (rad/s) for spin
    wx: float = 0.0
    wy: float = 0.0
    wz: float = 0.0

    # Covariance (uncertainty)
    covariance: Optional[np.ndarray] = None


class ExtendedKalmanFilter:
    """
    PROPRIETARY: Extended Kalman Filter with full physics model

    State vector (9D):
    [x, y, z, vx, vy, vz, wx, wy, wz]

    Incorporates:
    - Gravity (9.81 m/s²)
    - Quadratic drag (Cd = 0.47 for sphere)
    - Magnus effect for spin
    - Adaptive noise estimation
    - Outlier rejection
    """

    def __init__(
        self,
        initial_state: BallState,
        dt: float = 1/60.0,  # Time step (60 fps default)
        ball_mass: float = 0.43,  # Soccer ball mass (kg)
        ball_radius: float = 0.11,  # Soccer ball radius (m)
        air_density: float = 1.225,  # Air density (kg/m³)
        drag_coefficient: float = 0.47,  # Sphere drag coefficient
        magnus_coefficient: float = 0.00001  # Magnus force coefficient
    ):
        self.dt = dt
        self.ball_mass = ball_mass
        self.ball_radius = ball_radius
        self.air_density = air_density
        self.drag_coefficient = drag_coefficient
        self.magnus_coefficient = magnus_coefficient

        # Gravitational acceleration
        self.g = 9.81  # m/s²

        # Cross-sectional area
        self.area = np.pi * ball_radius**2

        # State vector: [x, y, z, vx, vy, vz, wx, wy, wz]
        self.state = np.array([
            initial_state.x, initial_state.y, initial_state.z,
            initial_state.vx, initial_state.vy, initial_state.vz,
            initial_state.wx, initial_state.wy, initial_state.wz
        ])

        # State covariance matrix (9x9)
        self.P = np.eye(9) * 100.0

        # Process noise covariance (tuned for soccer ball dynamics)
        self.Q = np.diag([
            0.01, 0.01, 0.01,  # Position uncertainty
            0.5, 0.5, 0.5,     # Velocity uncertainty
            0.1, 0.1, 0.1      # Angular velocity uncertainty
        ])

        # Measurement noise covariance (3D position measurements)
        self.R = np.diag([
            1.0, 1.0, 1.0  # Position measurement uncertainty
        ])

        # Outlier rejection threshold (Mahalanobis distance)
        self.outlier_threshold = 3.0

    def predict(self) -> BallState:
        """
        PROPRIETARY: Prediction step with full physics model

        Implements non-linear motion model:
        - F_gravity = m * g
        - F_drag = -0.5 * ρ * Cd * A * v² * v_hat
        - F_magnus = Cl * ρ * A * v * (ω × v)

        Returns:
            Predicted state
        """

        # Extract current state
        x, y, z = self.state[0:3]
        vx, vy, vz = self.state[3:6]
        wx, wy, wz = self.state[6:9]

        # Velocity magnitude
        v = np.sqrt(vx**2 + vy**2 + vz**2)

        # Drag force (opposes velocity)
        if v > 0.001:  # Avoid division by zero
            drag_magnitude = 0.5 * self.air_density * self.drag_coefficient * self.area * v**2
            drag_accel = -drag_magnitude / self.ball_mass * np.array([vx, vy, vz]) / v
        else:
            drag_accel = np.zeros(3)

        # Magnus force (perpendicular to velocity and spin)
        omega = np.array([wx, wy, wz])
        velocity = np.array([vx, vy, vz])
        magnus_force = self.magnus_coefficient * np.cross(omega, velocity)
        magnus_accel = magnus_force / self.ball_mass

        # Gravity (acts downward, assuming z is vertical)
        gravity_accel = np.array([0, 0, -self.g])

        # Total acceleration
        total_accel = drag_accel + magnus_accel + gravity_accel

        # Update state using Euler integration (could use RK4 for better accuracy)
        new_x = x + vx * self.dt
        new_y = y + vy * self.dt
        new_z = z + vz * self.dt

        new_vx = vx + total_accel[0] * self.dt
        new_vy = vy + total_accel[1] * self.dt
        new_vz = vz + total_accel[2] * self.dt

        # Angular velocity decays due to air resistance
        spin_decay = 0.99  # 1% decay per frame
        new_wx = wx * spin_decay
        new_wy = wy * spin_decay
        new_wz = wz * spin_decay

        # Update state vector
        self.state = np.array([
            new_x, new_y, new_z,
            new_vx, new_vy, new_vz,
            new_wx, new_wy, new_wz
        ])

        # Calculate Jacobian of state transition (for EKF)
        F = self._calculate_jacobian()

        # Update covariance: P = F * P * F' + Q
        self.P = F @ self.P @ F.T + self.Q

        return BallState(
            x=new_x, y=new_y, z=new_z,
            vx=new_vx, vy=new_vy, vz=new_vz,
            wx=new_wx, wy=new_wy, wz=new_wz,
            covariance=self.P.copy()
        )

    def update(
        self,
        measurement: np.ndarray,
        measurement_type: str = '3d'
    ) -> BallState:
        """
        PROPRIETARY: Measurement update with outlier rejection

        Args:
            measurement: Observed position [x, y, z] or [x, y] for 2D
            measurement_type: '3d' or '2d'

        Returns:
            Updated state after incorporating measurement
        """

        if measurement_type == '2d':
            # Only x, y measurements available (z unknown)
            H = np.zeros((2, 9))
            H[0, 0] = 1.0  # x
            H[1, 1] = 1.0  # y
            z = measurement[:2]
            R = self.R[:2, :2]
        else:
            # Full 3D measurement
            H = np.zeros((3, 9))
            H[0, 0] = 1.0  # x
            H[1, 1] = 1.0  # y
            H[2, 2] = 1.0  # z
            z = measurement[:3]
            R = self.R

        # Innovation (measurement residual)
        y = z - H @ self.state

        # Innovation covariance
        S = H @ self.P @ H.T + R

        # Mahalanobis distance for outlier detection
        mahal_dist = np.sqrt(y.T @ np.linalg.inv(S) @ y)

        if mahal_dist > self.outlier_threshold:
            # Measurement is an outlier, skip update
            return BallState(
                x=self.state[0], y=self.state[1], z=self.state[2],
                vx=self.state[3], vy=self.state[4], vz=self.state[5],
                wx=self.state[6], wy=self.state[7], wz=self.state[8],
                covariance=self.P.copy()
            )

        # Kalman gain
        K = self.P @ H.T @ np.linalg.inv(S)

        # Update state
        self.state = self.state + K @ y

        # Update covariance: P = (I - K*H) * P
        I = np.eye(9)
        self.P = (I - K @ H) @ self.P

        return BallState(
            x=self.state[0], y=self.state[1], z=self.state[2],
            vx=self.state[3], vy=self.state[4], vz=self.state[5],
            wx=self.state[6], wy=self.state[7], wz=self.state[8],
            covariance=self.P.copy()
        )

    def _calculate_jacobian(self) -> np.ndarray:
        """
        Calculate Jacobian of state transition function

        For linearization of non-linear dynamics around current state.
        """

        # Extract current state
        vx, vy, vz = self.state[3:6]
        v = np.sqrt(vx**2 + vy**2 + vz**2)

        # Initialize Jacobian (9x9)
        F = np.eye(9)

        # Position derivatives
        F[0, 3] = self.dt  # dx/dvx
        F[1, 4] = self.dt  # dy/dvy
        F[2, 5] = self.dt  # dz/dvz

        # Velocity derivatives (complex due to drag and Magnus)
        # Simplified linearization around current velocity
        if v > 0.001:
            drag_factor = (0.5 * self.air_density * self.drag_coefficient *
                          self.area * v / self.ball_mass)

            # Drag affects velocity (non-linear, linearized)
            F[3, 3] = 1 - drag_factor * self.dt
            F[4, 4] = 1 - drag_factor * self.dt
            F[5, 5] = 1 - drag_factor * self.dt - self.g * self.dt / v

        # Angular velocity decays
        spin_decay = 0.99
        F[6, 6] = spin_decay
        F[7, 7] = spin_decay
        F[8, 8] = spin_decay

        return F

    def get_current_state(self) -> BallState:
        """Get current state estimate"""
        return BallState(
            x=self.state[0], y=self.state[1], z=self.state[2],
            vx=self.state[3], vy=self.state[4], vz=self.state[5],
            wx=self.state[6], wy=self.state[7], wz=self.state[8],
            covariance=self.P.copy()
        )

    def estimate_spin_from_trajectory(
        self,
        trajectory_deviation: np.ndarray
    ) -> Tuple[float, np.ndarray]:
        """
        PROPRIETARY: Estimate spin rate and axis from trajectory curvature

        Uses Magnus effect model to infer spin from lateral deviation

        Args:
            trajectory_deviation: Lateral deviation from parabolic path

        Returns:
            (spin_rate_rpm, spin_axis_vector)
        """

        # Analyze deviation pattern
        max_deviation = np.max(np.abs(trajectory_deviation))

        if max_deviation < 0.01:  # Less than 1cm deviation
            return 0.0, np.array([0, 0, 0])

        # Estimate spin rate from deviation magnitude
        # Magnus force: F = Cl * ρ * A * v * r * ω
        # Simplified: ω ≈ deviation / (Cl * ρ * A * v * r)

        v_avg = np.linalg.norm([self.state[3], self.state[4], self.state[5]])
        if v_avg < 0.1:
            return 0.0, np.array([0, 0, 0])

        # Rough spin estimation (empirical)
        spin_rate_rads = max_deviation * 10.0 / (self.ball_radius * v_avg)
        spin_rate_rpm = spin_rate_rads * 60.0 / (2 * np.pi)

        # Determine spin axis from deviation direction
        # Simplified: check if deviation is horizontal or vertical
        horizontal_dev = trajectory_deviation[0]
        vertical_dev = trajectory_deviation[1] if len(trajectory_deviation) > 1 else 0

        if abs(horizontal_dev) > abs(vertical_dev):
            # Sidespin
            spin_axis = np.array([0, 0, 1]) if horizontal_dev > 0 else np.array([0, 0, -1])
        else:
            # Topspin/backspin
            spin_axis = np.array([1, 0, 0]) if vertical_dev > 0 else np.array([-1, 0, 0])

        return float(spin_rate_rpm), spin_axis

    def adaptive_noise_estimation(
        self,
        innovation_history: list
    ):
        """
        PROPRIETARY: Adaptive noise covariance estimation

        Adjusts Q and R based on innovation statistics for optimal filtering

        Args:
            innovation_history: Recent innovation (residual) values
        """

        if len(innovation_history) < 10:
            return

        # Calculate innovation statistics
        innovations = np.array(innovation_history[-10:])
        innovation_cov = np.cov(innovations.T)

        # Adapt measurement noise based on innovation
        # If innovations are large, increase R
        innovation_norm = np.trace(innovation_cov)

        if innovation_norm > 10.0:
            # Measurements are noisy, increase R
            self.R *= 1.1
        elif innovation_norm < 1.0:
            # Measurements are good, decrease R
            self.R *= 0.95

        # Clamp R to reasonable range
        self.R = np.clip(self.R, 0.1, 10.0)
