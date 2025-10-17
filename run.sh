#!/bin/bash

# KickSpeed Pro - Start Script

echo "🚀 Starting KickSpeed Pro..."
echo ""

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    echo "📥 Installing Python dependencies..."
    pip install -r requirements.txt
    cd ..
else
    echo "✅ Python environment found"
fi

# Check if node_modules exists
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    cd frontend
    npm install
    cd ..
else
    echo "✅ Node modules found"
fi

echo ""
echo "🎯 Starting services..."
echo ""

# Start backend
echo "🔧 Starting Backend API on http://localhost:8000"
cd backend
source venv/bin/activate
python -m app.main &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Frontend on http://localhost:3000"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✨ KickSpeed Pro is running!"
echo ""
echo "📊 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📖 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait

