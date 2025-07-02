# OGPW Deployment Guide

## Quick Start Options

### Option 1: Windows Batch Script
```bash
# Double-click or run in Command Prompt
start.bat
```

### Option 2: Linux/Mac Shell Script
```bash
# Make executable and run
chmod +x start.sh
./start.sh
```

### Option 3: Manual Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
python app.py

# Frontend (in new terminal)
npm install
npm run dev
```

### Option 4: Docker Compose
```bash
docker-compose up --build
```

## Environment Configuration

1. Copy `backend/.env.example` to `backend/.env`
2. Add your OpenAI API key (optional):
   ```
   OPENAI_API_KEY=your_key_here
   ```

## Production Deployment

### Using Docker
```bash
# Build and run
docker-compose -f docker-compose.prod.yml up --build -d

# View logs
docker-compose logs -f
```

### Manual Production Setup
```bash
# Backend
cd backend
pip install -r requirements.txt
gunicorn --bind 0.0.0.0:5000 app:app

# Frontend
npm run build
npm run preview
```

## Troubleshooting

- **Port 5000 in use**: Change backend port in `app.py`
- **Python dependencies fail**: Ensure Python 3.8+ is installed
- **Node dependencies fail**: Ensure Node.js 16+ is installed
- **PCAP upload fails**: Check file size (max 500MB) and format

## Security Notes

- Change default ports in production
- Use environment variables for sensitive data
- Enable HTTPS in production
- Implement proper authentication if needed