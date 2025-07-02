#!/bin/bash

echo "Starting OGPW - AI Network Traffic Analysis Platform"
echo

echo "Installing Python dependencies..."
cd backend
python3 -m pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install Python dependencies"
    exit 1
fi

echo
echo "Starting backend server..."
python3 app.py &
BACKEND_PID=$!

echo "Backend started with PID: $BACKEND_PID"
echo "Waiting for backend to initialize..."
sleep 3

cd ..
echo "Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    echo "Failed to install Node.js dependencies"
    kill $BACKEND_PID
    exit 1
fi

echo
echo "Starting frontend development server..."
npm run dev

# Clean up backend process when script exits
trap "kill $BACKEND_PID" EXIT