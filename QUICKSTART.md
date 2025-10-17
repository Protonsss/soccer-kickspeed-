# Quick Start

Want to get this running fast? Here's how.

## What you need first

Install these if you haven't already:
- Python 3.9+ ([get it here](https://www.python.org/downloads/))
- Node.js 18+ ([get it here](https://nodejs.org/))

## Easiest way to start

I made a script that handles everything:

**Mac or Linux:**
```bash
chmod +x run.sh && ./run.sh
```

**Windows:**
```cmd
run.bat
```

The script will install everything and start the app. Give it a minute or two on first run - it needs to download dependencies. Once it's done, open `http://localhost:3000` in your browser.

## If the script doesn't work

Do it manually in two terminals:

**Terminal 1:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows folks use: venv\Scripts\activate
pip install -r requirements.txt
python -m app.main
```

**Terminal 2:**
```bash
cd frontend
npm install
npm run dev
```

## Try it out

1. Open `http://localhost:3000` in your browser
2. Drag a video file onto the upload area (or click to browse)
3. Hit "Analyze Kick"
4. Wait about 10-30 seconds
5. Check out your results

## Recording tips

Your video quality directly affects the results. Here's what works:
- Record from the side so you can see the full ball path
- Use decent lighting - outdoor daylight is perfect
- Keep it short, 2-10 seconds
- If you can get the goal posts in frame, do it - helps with calibration
- 720p minimum, 1080p is better
- 60fps if your phone/camera supports it

## What you'll get

The app breaks down your kick into:
- **Speed metrics** - Max speed, average, how it changes over time
- **Shot placement** - Where it would land on the goal, with a visual heat map
- **Trajectory data** - Launch angle, height, distance, arc type
- **Power analysis** - Strike quality rating and estimated foot speed
- **Spin detection** - RPM and which way it's spinning
- **Timing info** - Flight time and frame-by-frame tracking

## Common problems

**"Port already in use"**

Something else is using port 8000 or 3000. Kill it:
```bash
# Mac/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**"Module not found" errors**

Dependencies didn't install right. Try again:
```bash
# Backend
cd backend && pip install -r requirements.txt

# Frontend
cd frontend && npm install
```

**"Could not track ball"**

The AI is having trouble seeing the ball. Usually means:
- Lighting is too dark
- Ball is too small in frame
- Too much motion blur
- Camera angle is weird

Try recording in better light, closer to the action, or with a higher frame rate.

## Want to know more?

- Full docs are in [README.md](README.md)
- Detailed setup help in [SETUP.md](SETUP.md)
- How the algorithms work in [ALGORITHMS.md](ALGORITHMS.md)

Got stuck? Open an issue on GitHub and I'll help you out.

---

That's it. Go analyze some kicks.

