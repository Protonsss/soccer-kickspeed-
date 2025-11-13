# KickSpeed Pro

Ever wanted to know exactly how fast your soccer kick is? Or where it would land on the goal? This project does exactly that using computer vision and AI.

I built this to analyze soccer kicks with the same level of detail you'd get from professional sports labs. It measures speed, trajectory, placement, spin, power - basically everything you'd want to know about your shot.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.9+-green)
![Next.js](https://img.shields.io/badge/next.js-14.0-black)

## What it does

The app analyzes your kick videos and gives you:

**Speed tracking** - Maximum speed, average speed, and how it changes through the air (in both km/h and mph)

**Shot placement** - Shows exactly where your shot would land on the goal with a heat map. It'll tell you if you hit top corner or if you're wide left.

**Trajectory analysis** - Launch angle, max height, distance traveled, and what kind of arc your shot has

**Spin detection** - Estimates the RPM and direction of spin on the ball

**Power metrics** - Calculates the strike quality and even estimates your foot speed

**Timing data** - Flight time and frame-by-frame tracking of the ball

## Tech behind it

I used some pretty cool tech to make this work:
- YOLOv8 for detecting the ball (it's really good at finding soccer balls in video)
- Kalman filters to smooth out the tracking and handle when the ball gets partially hidden
- PyTorch for the AI stuff
- FastAPI for a fast backend
- Next.js for a clean, responsive frontend

The system uses multiple detection methods at once - if one fails, another picks up the slack. This is why it's so accurate.

## What you need

**For the backend:**
- Python 3.9 or newer
- A GPU helps but isn't required (it'll just run a bit slower without one)

**For the frontend:**
- Node.js 18 or newer
- npm or yarn

## Getting started

### Easy way (recommended)

I made scripts that do everything automatically:

**On Mac/Linux:**
```bash
./run.sh
```

**On Windows:**
```bash
run.bat
```

That's it. The script installs dependencies and starts both the backend and frontend for you.

### Manual setup

If you prefer to do it yourself:

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows users: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

**Frontend (open a new terminal):**
```bash
cd frontend
npm install
npm run dev
```

Then open `http://localhost:3000` in your browser. Upload a video of a soccer kick and wait about 10-30 seconds for the analysis.

## The details

Here's everything the app measures:

**Speed**
- How fast the ball is traveling at its peak
- Average speed during flight
- Initial velocity right after contact
- Speed when it reaches the goal

**Trajectory**
- Launch angle (how steep you kicked it)
- Maximum height the ball reaches
- Total distance traveled
- Whether it's a ground shot, low drive, or high arc
- How smooth and consistent the path is

**Shot placement**
- Which part of the goal you'd hit (top corner, center, etc.)
- Whether you actually score or miss
- How far off-center the shot is
- An accuracy score from 0-100

**Power**
- Estimated foot speed at impact
- Kinetic energy in Joules
- Overall strike quality (perfect, good, average, or poor)
- Type of contact (instep, laces, toe, etc.)

**Spin**
- Rotation speed in RPM
- Spin direction (topspin, backspin, or sidespin)
- Spin efficiency

**Timing**
- Total flight time
- Time from kick to goal
- Frame-by-frame position data

## Tips for recording

The better your video, the better the analysis. Here's what works best:

- **Format**: MP4, MOV, AVI, MKV, or WebM all work
- **Frame rate**: 30fps minimum, but 60fps gives way better results
- **Quality**: 720p or higher. 1080p is ideal.
- **Length**: Keep it short - 2 to 10 seconds is perfect
- **Lighting**: Shoot during the day or with good lights. Avoid shadows.
- **Camera angle**: Side view works best. You want to see the entire ball path from kick to goal.
- **Background**: If you can get the goal posts in frame, the app will auto-calibrate and be more accurate

## How it works

Here's what happens when you upload a video:

1. The backend splits your video into individual frames
2. YOLOv8 (an AI model) scans each frame to find the soccer ball
3. If YOLOv8 misses the ball, a backup color-detection system kicks in
4. A Kalman filter smooths out the tracking and handles when the ball is briefly hidden
5. The system calibrates itself by detecting the goal posts (or you can set a manual distance)
6. Physics algorithms calculate speed, trajectory, spin, and all the other metrics
7. Everything gets packaged up and sent to the frontend
8. You see beautiful charts and visualizations of your kick

The multi-method approach is key - by using both AI detection and traditional computer vision, the system rarely loses track of the ball.

## Configuration

You can tweak settings in `backend/app/core/config.py`:
- Database connection
- Where uploaded videos are stored
- Detection confidence thresholds
- Goal post dimensions (if you're not using standard FIFA goals)

For environment-specific settings, create a `backend/.env` file:
```env
DATABASE_URL=sqlite:///./kickspeed.db
SECRET_KEY=your-secret-key
MAX_FILE_SIZE=100000000
CONFIDENCE_THRESHOLD=0.5
```

## API

If you want to integrate this into something else, there's a REST API:

**POST /api/analyze** - Send a video file, get back analysis results

**GET /health** - Check if the server is running

**GET /docs** - Interactive API documentation (visit http://localhost:8000/docs when the backend is running)

## Contributing

Found a bug? Want to add a feature? Pull requests are welcome. This started as a personal project but I'm happy to collaborate.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

Feel free to use, modify, and distribute this code. Contributions and forks are welcome!

## Thanks

This wouldn't exist without some amazing open-source projects:
- Ultralytics for YOLOv8
- The PyTorch team
- OpenCV community
- FastAPI and Next.js

## Questions?

Open an issue on GitHub if you run into problems or have ideas for improvements.

---

Built for soccer players who are curious about their technique and want real data to improve.
