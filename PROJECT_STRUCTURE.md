# 📁 KickSpeed Pro - Project Structure

Complete overview of the project architecture and file organization.

## Root Directory

```
Kickspeed/
├── README.md              # Main project documentation
├── QUICKSTART.md         # 5-minute getting started guide
├── SETUP.md              # Detailed setup instructions
├── ALGORITHMS.md         # Technical algorithms explained
├── PROJECT_STRUCTURE.md  # This file
├── .gitignore            # Git ignore rules
├── run.sh                # Start script (macOS/Linux)
├── run.bat               # Start script (Windows)
│
├── backend/              # Python FastAPI backend
│   ├── README.md
│   ├── requirements.txt
│   ├── .gitignore
│   ├── .env.example
│   ├── uploads/          # Video upload directory (created on first run)
│   └── app/
│       ├── __init__.py
│       ├── main.py       # FastAPI application entry point
│       │
│       ├── core/         # Core configuration
│       │   ├── __init__.py
│       │   └── config.py
│       │
│       ├── models/       # Data models
│       │   ├── __init__.py
│       │   └── schemas.py
│       │
│       ├── database/     # Database layer
│       │   ├── __init__.py
│       │   ├── database.py
│       │   └── models.py
│       │
│       └── analysis/     # Core analysis modules
│           ├── __init__.py
│           ├── video_processor.py
│           ├── ball_tracker.py
│           └── metrics_calculator.py
│
└── frontend/             # Next.js React frontend
    ├── README.md
    ├── package.json
    ├── tsconfig.json
    ├── next.config.js
    ├── tailwind.config.ts
    ├── postcss.config.js
    ├── .gitignore
    │
    └── src/
        ├── app/          # Next.js 14 App Router
        │   ├── layout.tsx
        │   ├── page.tsx
        │   └── globals.css
        │
        ├── components/   # React components
        │   ├── Header.tsx
        │   ├── Hero.tsx
        │   ├── VideoUploader.tsx
        │   ├── AnalysisResults.tsx
        │   ├── MetricsOverview.tsx
        │   ├── SpeedChart.tsx
        │   ├── TrajectoryVisualization.tsx
        │   ├── GoalPlacement.tsx
        │   └── DetailedMetrics.tsx
        │
        └── types/        # TypeScript type definitions
            └── index.ts
```

## Backend Architecture

### Entry Point: `app/main.py`
- FastAPI application setup
- CORS middleware configuration
- API endpoint definitions
- Error handling

### Core Modules

#### `app/analysis/video_processor.py`
**Purpose**: Video file handling and frame extraction

**Key Functions**:
- `extract_video_info()` - Get video metadata
- `extract_frames()` - Extract frames from video
- `preprocess_frame()` - Prepare frames for analysis
- `apply_frame_interpolation()` - Increase temporal resolution

#### `app/analysis/ball_tracker.py`
**Purpose**: Ball detection and tracking

**Key Components**:
- YOLOv8 model integration
- Kalman filter implementation
- Color-based fallback detection
- Optical flow tracking (placeholder)
- Multi-method fusion strategy

**Key Functions**:
- `track_ball()` - Main tracking pipeline
- `_detect_ball_yolo()` - YOLO detection
- `_detect_ball_color()` - Color-based detection
- `_init_kalman_filter()` - Kalman setup
- `_calculate_tracking_quality()` - Quality metrics

#### `app/analysis/metrics_calculator.py`
**Purpose**: Calculate all analysis metrics

**Key Functions**:
- `calculate_all_metrics()` - Main calculation pipeline
- `_calculate_speed_metrics()` - Speed analysis
- `_calculate_trajectory_metrics()` - Trajectory analysis
- `_calculate_spin_metrics()` - Spin estimation
- `_calculate_placement_metrics()` - Shot placement
- `_calculate_power_metrics()` - Power analysis
- `_calculate_timing_metrics()` - Timing data
- `_calculate_overall_score()` - Composite score

### Data Models

#### `app/models/schemas.py`
Pydantic models for request/response validation:
- `VideoInfo` - Video metadata
- `BallPosition` - Frame-by-frame ball position
- `SpeedMetrics` - Speed analysis results
- `TrajectoryMetrics` - Trajectory data
- `SpinMetrics` - Spin analysis
- `PlacementMetrics` - Placement data
- `PowerMetrics` - Power analysis
- `TimingMetrics` - Timing information
- `ComprehensiveMetrics` - All metrics combined
- `AnalysisResponse` - API response structure

### Database

#### `app/database/models.py`
SQLAlchemy models for data persistence:
- `KickAnalysis` - Store analysis results

#### `app/database/database.py`
- Database connection setup
- Session management
- Engine configuration

### Configuration

#### `app/core/config.py`
- Environment variables
- Default settings
- Calibration constants
- Thresholds and parameters

## Frontend Architecture

### Pages

#### `src/app/page.tsx`
**Main Application Page**
- State management for analysis flow
- Orchestrates VideoUploader and AnalysisResults
- Hero section display

#### `src/app/layout.tsx`
**Root Layout**
- HTML document structure
- Global styles import
- Metadata configuration

### Components

#### `src/components/Header.tsx`
**Navigation Header**
- Logo and branding
- Status indicators

#### `src/components/Hero.tsx`
**Landing Section**
- Feature highlights
- Animated cards
- Value proposition

#### `src/components/VideoUploader.tsx`
**Upload Interface**
- Drag-and-drop functionality
- File validation
- Upload progress tracking
- API communication
- Error handling

#### `src/components/AnalysisResults.tsx`
**Results Dashboard**
- Overall score display
- Component orchestration
- Download/share functionality

#### `src/components/MetricsOverview.tsx`
**Quick Metrics Cards**
- 6 key metric cards
- Animated entrance
- Gradient styling
- Icon integration

#### `src/components/SpeedChart.tsx`
**Speed Visualization**
- Line chart with Recharts
- Speed over time
- Interactive tooltips
- Summary statistics

#### `src/components/TrajectoryVisualization.tsx`
**Trajectory Plot**
- Scatter chart with path
- Frame-by-frame positions
- Confidence indicators
- Smoothness metrics

#### `src/components/GoalPlacement.tsx`
**Placement Heat Map**
- Goal grid visualization
- Impact point marker
- Zone classification
- Accuracy scoring

#### `src/components/DetailedMetrics.tsx`
**Comprehensive Data**
- All metrics organized by category
- Professional comparisons
- Video information
- Detailed breakdowns

### Types

#### `src/types/index.ts`
TypeScript interfaces matching backend schemas:
- All metric interfaces
- Analysis data structures
- Component prop types

### Styling

#### `src/app/globals.css`
- TailwindCSS directives
- Custom animations
- Glass morphism effects
- Scrollbar styling

#### `tailwind.config.ts`
- Color palette
- Theme extensions
- Animation definitions
- Plugin configuration

## Data Flow

### Analysis Pipeline

```
1. User uploads video
   ↓
2. Frontend sends to /api/analyze
   ↓
3. Backend saves file
   ↓
4. video_processor extracts frames & metadata
   ↓
5. ball_tracker detects and tracks ball
   ↓
6. metrics_calculator computes all metrics
   ↓
7. Response sent to frontend
   ↓
8. Frontend displays results with visualizations
```

### Technology Stack

**Backend**:
- **FastAPI**: Modern async web framework
- **PyTorch**: Deep learning framework
- **Ultralytics YOLOv8**: Object detection
- **OpenCV**: Computer vision operations
- **FilterPy**: Kalman filtering
- **SciPy**: Scientific computing
- **NumPy**: Numerical operations
- **SQLAlchemy**: Database ORM

**Frontend**:
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **TailwindCSS**: Utility-first CSS
- **Framer Motion**: Animation library
- **Recharts**: Chart library
- **Axios**: HTTP client
- **Lucide Icons**: Icon library

## API Endpoints

### `POST /api/analyze`
Upload and analyze video

**Request**: multipart/form-data
- `video`: Video file
- `reference_distance`: Optional[float]
- `use_goal_calibration`: bool

**Response**: JSON
- Complete analysis results

### `POST /api/quick-analyze`
Quick analysis with defaults

### `DELETE /api/analysis/{analysis_id}`
Delete analysis and files

### `GET /health`
Health check endpoint

### `GET /`
API information

## Configuration Files

### Backend
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `.gitignore` - Git ignore patterns

### Frontend
- `package.json` - Node dependencies and scripts
- `tsconfig.json` - TypeScript configuration
- `next.config.js` - Next.js configuration
- `tailwind.config.ts` - Tailwind customization
- `postcss.config.js` - PostCSS plugins
- `.gitignore` - Git ignore patterns

## Development Workflow

### Backend Development
```bash
cd backend
source venv/bin/activate
python -m app.main  # Start with auto-reload
```

### Frontend Development
```bash
cd frontend
npm run dev  # Start with hot-reload
```

### Making Changes

**Backend**:
1. Modify Python files
2. Server auto-reloads
3. Test at http://localhost:8000/docs

**Frontend**:
1. Modify TSX/CSS files
2. Fast Refresh updates instantly
3. Test at http://localhost:3000

## Deployment Considerations

### Backend
- Use production ASGI server (Gunicorn + Uvicorn)
- Set proper environment variables
- Configure database connection
- Set up file storage (S3, etc.)
- Enable HTTPS
- Rate limiting
- Authentication

### Frontend
- Build: `npm run build`
- Deploy to Vercel, Netlify, or custom server
- Update API endpoint URL
- Configure environment variables
- Enable analytics

## Future Extensions

Potential areas for expansion:
- User authentication system
- Historical analysis database
- Real-time camera analysis
- Mobile app (React Native)
- Team management features
- Social sharing
- Leaderboards
- Training recommendations
- Multi-angle analysis
- 3D trajectory reconstruction

---

**This structure provides a solid foundation for professional soccer kick analysis!**

