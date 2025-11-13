"""
PROPRIETARY - Advanced Analysis Modules
Copyright (c) 2025 Stephen Chen. All Rights Reserved.

Enterprise-grade computer vision and physics algorithms.

CONFIDENTIAL - Contains trade secrets and proprietary methods.
Unauthorized access, use, or distribution is strictly prohibited.
"""

from .camera_calibration import AdvancedCameraCalibrator, CameraParameters
from .reconstruction_3d import MultiViewReconstructor, Point3D, Trajectory3D
from .extended_kalman import ExtendedKalmanFilter, BallState
from .subpixel_detector import SubPixelDetector
from .spin_analyzer import AdvancedSpinAnalyzer, SpinAnalysis
from .physics_engine import AdvancedPhysicsEngine, AerodynamicForces

__all__ = [
    'AdvancedCameraCalibrator',
    'CameraParameters',
    'MultiViewReconstructor',
    'Point3D',
    'Trajectory3D',
    'ExtendedKalmanFilter',
    'BallState',
    'SubPixelDetector',
    'AdvancedSpinAnalyzer',
    'SpinAnalysis',
    'AdvancedPhysicsEngine',
    'AerodynamicForces',
]

# Version
__version__ = '1.0.0-enterprise'
__author__ = 'Stephen Chen'
__license__ = 'Proprietary'
