#!/bin/bash

echo "Starting Project Canary Backend..."
echo ""

if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and add your Supabase credentials"
    exit 1
fi

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Starting FastAPI server..."
echo "Server will be available at http://localhost:8000"
echo ""

python main.py
