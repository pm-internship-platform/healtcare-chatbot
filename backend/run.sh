#!/bin/bash
# Activate virtual environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Run FastAPI app
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
