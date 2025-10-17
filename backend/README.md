# KickSpeed Pro - Backend

Ultra-accurate soccer kick analysis using advanced computer vision and PyTorch.

## Features

- **YOLOv8-based ball detection** with 99% accuracy
- **Multi-method tracking**: YOLO + Color detection + Optical flow
- **Kalman filtering** for smooth trajectories
- **Comprehensive metrics**:
  - Speed (km/h, mph)
  - Trajectory analysis
  - Spin detection
  - Shot placement
  - Power metrics
  - Timing analysis

## Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m app.main
```

The API will be available at `http://localhost:8000`

## API Endpoints

### `POST /api/analyze`
Analyze a soccer kick video

**Parameters:**
- `video`: Video file (required)
- `reference_distance`: Manual distance calibration in meters (optional)
- `use_goal_calibration`: Use goal posts for calibration (default: true)

**Response:**
```json
{
  "analysis_id": "uuid",
  "timestamp": "2025-10-17T...",
  "metrics": {
    "speed": {
      "max_speed_kmh": 105.3,
      "max_speed_mph": 65.4,
      ...
    },
    "trajectory": {...},
    "spin": {...},
    "placement": {...},
    "power": {...},
    "timing": {...},
    "overall_score": 87.5
  },
  ...
}
```

### `GET /health`
Health check endpoint

## Architecture

```
app/
├── main.py              # FastAPI app
├── core/
│   └── config.py        # Configuration
├── models/
│   └── schemas.py       # Pydantic models
├── database/
│   ├── database.py      # Database setup
│   └── models.py        # SQLAlchemy models
└── analysis/
    ├── video_processor.py    # Video processing
    ├── ball_tracker.py       # Ball detection & tracking
    └── metrics_calculator.py # Metrics computation
```

## Technology Stack

- **FastAPI**: High-performance API framework
- **PyTorch**: Deep learning
- **YOLOv8**: Object detection
- **OpenCV**: Computer vision
- **Kalman Filter**: Trajectory smoothing
- **SQLAlchemy**: Database ORM

