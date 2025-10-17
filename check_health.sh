#!/bin/bash

# KickSpeed Pro - Health Check Script
# Tests if backend and frontend are running correctly

echo "🏥 KickSpeed Pro Health Check"
echo "=============================="
echo ""

# Check Backend
echo "🔧 Checking Backend API..."
BACKEND_RESPONSE=$(curl -s http://localhost:8000/health)
if [ $? -eq 0 ]; then
    echo "✅ Backend is running"
    echo "   Response: $BACKEND_RESPONSE"
else
    echo "❌ Backend is not responding"
    echo "   Make sure to start the backend first:"
    echo "   cd backend && source venv/bin/activate && python -m app.main"
fi

echo ""

# Check Frontend
echo "🎨 Checking Frontend..."
FRONTEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000)
if [ "$FRONTEND_RESPONSE" = "200" ]; then
    echo "✅ Frontend is running"
    echo "   HTTP Status: $FRONTEND_RESPONSE"
else
    echo "❌ Frontend is not responding"
    echo "   Make sure to start the frontend first:"
    echo "   cd frontend && npm run dev"
fi

echo ""
echo "=============================="

# Check Python
echo ""
echo "📋 System Requirements:"
echo ""
PYTHON_VERSION=$(python3 --version 2>&1)
echo "Python: $PYTHON_VERSION"

NODE_VERSION=$(node --version 2>&1)
echo "Node.js: $NODE_VERSION"

NPM_VERSION=$(npm --version 2>&1)
echo "npm: $NPM_VERSION"

echo ""
echo "📦 Backend Dependencies:"
if [ -f "backend/venv/bin/python" ]; then
    echo "✅ Virtual environment exists"
    TORCH_VERSION=$(backend/venv/bin/python -c "import torch; print(torch.__version__)" 2>&1)
    if [ $? -eq 0 ]; then
        echo "✅ PyTorch installed: $TORCH_VERSION"
    else
        echo "❌ PyTorch not installed"
    fi
    
    YOLO_VERSION=$(backend/venv/bin/python -c "import ultralytics; print(ultralytics.__version__)" 2>&1)
    if [ $? -eq 0 ]; then
        echo "✅ Ultralytics YOLO installed: $YOLO_VERSION"
    else
        echo "❌ Ultralytics not installed"
    fi
else
    echo "❌ Virtual environment not found"
fi

echo ""
echo "📦 Frontend Dependencies:"
if [ -d "frontend/node_modules" ]; then
    echo "✅ Node modules installed"
else
    echo "❌ Node modules not found - run: cd frontend && npm install"
fi

echo ""
echo "=============================="
echo ""

if [ "$BACKEND_RESPONSE" != "" ] && [ "$FRONTEND_RESPONSE" = "200" ]; then
    echo "✅ All systems operational!"
    echo ""
    echo "🚀 Open http://localhost:3000 to start analyzing!"
else
    echo "⚠️  Some services are not running"
    echo ""
    echo "Quick start:"
    echo "  ./run.sh"
fi

echo ""

