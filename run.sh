#!/bin/bash
# Helper script to run generate_forecast.py with venv

set -e

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found!"
    echo "Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Please edit .env and add your OPENAI_API_KEY"
        exit 1
    else
        echo "Please create .env file with: OPENAI_API_KEY=sk-your-key-here"
        exit 1
    fi
fi

# Run the script (it will load from .env automatically)
python scripts/generate_forecast.py

