# 🚀 KickSpeed Pro - Setup Guide

Complete setup instructions for getting KickSpeed Pro running on your machine.

## Prerequisites

Before you begin, ensure you have the following installed:

### Required
- **Python 3.9 or higher** - [Download](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

### Optional
- **CUDA-capable GPU** with CUDA toolkit for faster processing
- **FFmpeg** for advanced video processing (usually installed with OpenCV)

## Quick Start (Recommended)

### macOS / Linux
```bash
# Make run script executable (first time only)
chmod +x run.sh

# Start everything
./run.sh
```

### Windows
```cmd
# Double-click run.bat or run from command prompt
run.bat
```

The script will:
1. Create Python virtual environment (if needed)
2. Install all dependencies (if needed)
3. Start backend API server
4. Start frontend development server
5. Open your browser automatically

## Manual Setup

If you prefer to set up and run services manually:

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create uploads directory
mkdir uploads

# Start the server
python -m app.main
```

Backend will be available at: `http://localhost:8000`

### 2. Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: `http://localhost:3000`

## First Run

1. Open your browser and navigate to `http://localhost:3000`
2. You should see the KickSpeed Pro landing page
3. Upload a test video (or use sample video in `sample/` if available)
4. Wait for analysis to complete
5. View your comprehensive kick analysis!

## Troubleshooting

### Backend Issues

#### "ModuleNotFoundError: No module named 'torch'"
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install torch torchvision
```

#### "Could not load YOLO model"
The YOLOv8 model will download automatically on first use. If it fails:
```bash
cd backend
source venv/bin/activate
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"
```

#### Port 8000 already in use
```bash
# Find and kill the process using port 8000
# On macOS/Linux:
lsof -ti:8000 | xargs kill -9
# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Frontend Issues

#### "Module not found" errors
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### Port 3000 already in use
Edit `package.json` and change the dev script:
```json
"dev": "next dev -p 3001"
```

#### CORS errors
Ensure backend is running and accessible at `http://localhost:8000`

### Video Processing Issues

#### "Could not track ball reliably"
- Ensure video has good lighting
- Ball should be clearly visible
- Use higher frame rate videos (60fps+)
- Try different camera angles

#### Analysis takes too long
- Use shorter videos (2-5 seconds)
- Reduce video resolution
- Consider using GPU acceleration (CUDA)

## Performance Optimization

### Use GPU Acceleration (NVIDIA Only)

```bash
# Install CUDA toolkit from NVIDIA
# Then install PyTorch with CUDA support:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### Optimize Video Size

Before uploading, you can compress videos:
```bash
ffmpeg -i input.mp4 -vcodec h264 -acodec mp3 -vf scale=1280:720 output.mp4
```

## Production Deployment

### Backend (API)

1. Set environment variables:
```bash
export DATABASE_URL="postgresql://..."
export SECRET_KEY="your-production-secret"
```

2. Use production ASGI server:
```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend

1. Build for production:
```bash
cd frontend
npm run build
npm start
```

2. Or deploy to Vercel:
```bash
npm install -g vercel
vercel
```

## Testing

### Test Backend
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy","timestamp":"..."}
```

### Test API with Sample Video
```bash
curl -X POST http://localhost:8000/api/analyze \
  -F "video=@your_video.mp4" \
  -F "use_goal_calibration=true"
```

## Video Recording Tips

For best analysis results:

1. **Camera Position**: 
   - Side view or 45° angle
   - 10-20 meters from kick point
   - Stable tripod (no movement)

2. **Lighting**:
   - Good, even lighting
   - Avoid backlighting
   - Outdoor daylight is ideal

3. **Settings**:
   - 60+ fps if possible
   - 1080p resolution
   - Focus on ball, not kicker

4. **Frame the Shot**:
   - Include full ball trajectory
   - Show goal posts (for auto-calibration)
   - Ensure ball is always visible

## Next Steps

1. ✅ Run the application
2. 📹 Record or find a test video
3. 📤 Upload and analyze
4. 📊 Review metrics
5. 🎯 Improve your technique!

## Getting Help

- Check the main [README.md](README.md)
- Review [API documentation](http://localhost:8000/docs) when backend is running
- Open an issue on GitHub

## System Requirements

### Minimum
- **CPU**: Dual-core processor
- **RAM**: 4GB
- **Storage**: 2GB free space
- **OS**: Windows 10, macOS 10.15+, Linux

### Recommended
- **CPU**: Quad-core processor
- **RAM**: 8GB+
- **GPU**: NVIDIA GPU with CUDA support
- **Storage**: 5GB+ free space
- **OS**: Latest version

## What's Next?

After successful setup:
- Try analyzing different types of kicks
- Compare results over time
- Use metrics to improve technique
- Share results with teammates

Happy analyzing! ⚽🚀

