#!/bin/bash

# CourseCraft-AI Backend Startup Script

set -e

echo "🚀 Starting CourseCraft-AI Backend Setup..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed. Please install Python3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed. Please install pip3 first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing requirements..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p app/static/pdf
mkdir -p temp
mkdir -p logs

# Set environment variables (if .env exists)
if [ -f ".env" ]; then
    echo "🌍 Loading environment variables from .env..."
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "⚠️ No .env file found. Using default environment variables."
    echo "LLM_API_KEY=mock-key" > .env
    echo "EMBEDDING_MODEL=mock-embedding" >> .env
    echo "SESSION_TTL=86400" >> .env
    echo "Created .env file with default values."
fi

# Run tests (optional)
echo "🧪 Running tests..."
python -m pytest tests/ -v

# Start the application
echo "🚀 Starting CourseCraft-AI Backend..."
echo "🌐 API will be available at: http://localhost:8000"
echo "📚 API documentation at: http://localhost:8000/docs"
echo "💚 Health check at: http://localhost:8000/health"
echo ""

# Start the development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

echo "✅ CourseCraft-AI Backend is running!"