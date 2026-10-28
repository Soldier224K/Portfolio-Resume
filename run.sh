#!/usr/bin/env bash
set -e

echo "=========================================================="
echo "⚡ Starting AI Portfolio Management & Resume Generator"
echo "=========================================================="

# Check Python version
python3 --version

# Run database setup & start server
echo "Booting server on http://127.0.0.1:8000 ..."
python3 -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

