# OGPW - AI-Powered Network Traffic Analysis Platform

A comprehensive cybersecurity web application for PCAP (Packet Capture) analysis with AI-powered insights, anomaly detection, and natural language querying capabilities.

## 🚀 Features

- **PCAP File Analysis**: Upload and analyze .pcap/.pcapng files with detailed packet inspection (up to 500MB)
- **AI Assistant**: Natural language querying of network data using OpenAI integration
- **Interactive Dashboard**: Real-time visualizations of network traffic patterns and KPIs
- **Anomaly Detection**: Automatic identification of suspicious network activity
- **Protocol Filtering**: Filter and analyze traffic by specific protocols (TCP, UDP, DNS, HTTP, ICMP)
- **Export Reports**: Generate PDF and CSV reports of analysis results
- **Real-time Metrics**: TCP connection success rates, packet statistics, and performance indicators

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript
- **Tailwind CSS** for styling
- **Recharts** for data visualization
- **Axios** for API communication
- **React Dropzone** for file uploads

### Backend
- **Python Flask** REST API
- **Scapy** for packet analysis
- **OpenAI API** for AI assistant
- **ReportLab** for PDF generation
- **Pandas** for data processing

## 📋 Prerequisites

- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **OpenAI API Key** (optional, for AI features)

## 🚀 Quick Start (Windows)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ogpw
```

### 2. Frontend Setup
```bash
# Install frontend dependencies
npm install

# Start the frontend development server
npm run dev
```

### 3. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
python -m pip install -r requirements.txt

# Create environment file (optional for AI features)
copy .env.example .env
# Edit .env and add your OpenAI API key
```

### 4. Start the Backend Server
```bash
# From the backend directory
python app.py
```

### 5. Access the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000

## 🔧 Alternative Setup Methods

### Method 1: Run Everything with One Command
```bash
# Install all dependencies and start both servers
npm run setup-backend
npm run start-full
```

### Method 2: Manual Setup
1. **Frontend Only**:
   ```bash
   npm install
   npm run dev
   ```

2. **Backend Only**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python app.py
   ```

## 📁 Project Structure

```
ogpw/
├── backend/                 # Python Flask API
│   ├── app.py              # Main Flask application
│   ├── pcap_analyzer.py    # PCAP processing engine
│   ├── ai_assistant.py     # OpenAI integration
│   ├── utils.py            # Report generation utilities
│   └── requirements.txt    # Python dependencies
├── src/                    # React frontend
│   ├── components/         # React components
│   ├── services/          # API services
│   └── App.tsx            # Main application
├── package.json           # Node.js dependencies
└── README.md             # This file
```

## 🔑 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/upload` | POST | Upload PCAP file for analysis (max 500MB) |
| `/api/chat` | POST | Chat with AI assistant |
| `/api/analysis/current` | GET | Get current analysis data |
| `/api/analysis/filter` | POST | Filter packets by protocol |
| `/api/export/pdf` | GET | Export analysis as PDF |
| `/api/export/csv` | GET | Export analysis as CSV |
| `/api/health` | GET | Health check endpoint |

## 🤖 AI Assistant Configuration

To enable the AI assistant features:

1. Sign up for an OpenAI API key at https://platform.openai.com/
2. Copy `backend/.env.example` to `backend/.env`
3. Add your API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

**Note**: The application works without an OpenAI API key, but AI responses will use fallback pattern matching instead of advanced natural language processing.

## 📊 Supported PCAP Analysis

- **Basic Statistics**: Packet counts, bytes, duration, throughput
- **Protocol Distribution**: TCP, UDP, DNS, HTTP, ICMP analysis
- **IP Conversations**: Top communicating endpoints
- **TCP Streams**: Connection analysis and flow inspection
- **DNS Analysis**: Query/response patterns and domain statistics
- **Anomaly Detection**: Port scans, high-frequency traffic, suspicious patterns
- **KPI Monitoring**: Connection success rates, failure analysis

## 🔍 Example Use Cases

1. **Security Analysis**: Upload network captures to identify potential threats
2. **Performance Monitoring**: Analyze connection success rates and identify bottlenecks
3. **Incident Investigation**: Use AI assistant to query specific network events
4. **Educational**: Learn about network protocols through interactive analysis
5. **Compliance**: Generate reports for network security audits

## 📈 Dashboard Features

- **Real-time KPI Cards**: Packet counts, data transfer, connection metrics
- **Interactive Charts**: Protocol distribution, IP conversations, traffic timeline
- **Anomaly Alerts**: Automatically detected suspicious activities
- **TCP Stream Analysis**: Detailed connection flow inspection
- **Export Capabilities**: PDF and CSV reports for documentation

## 🛡️ Security Considerations

- PCAP files are processed locally and not stored permanently
- File uploads are limited to 500MB
- Only .pcap and .pcapng files are accepted
- API endpoints include basic error handling and validation

## 🔧 Troubleshooting

### Common Issues

1. **Backend won't start**:
   - Ensure Python 3.8+ is installed
   - Install requirements: `pip install -r backend/requirements.txt`
   - Check for port conflicts (Flask runs on port 5000)

2. **Frontend can't connect to backend**:
   - Verify backend is running on http://localhost:5000
   - Check CORS configuration in Flask app
   - Ensure no firewall blocking the connection

3. **PCAP upload fails**:
   - Check file size (max 500MB)
   - Ensure file is valid .pcap or .pcapng format
   - Verify sufficient disk space

4. **AI assistant not working**:
   - Check if OpenAI API key is configured
   - Verify API key has sufficient credits
   - Fallback responses will work without API key

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🔗 Additional Resources

- [Scapy Documentation](https://scapy.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [React Documentation](https://reactjs.org/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

For additional support or questions, please create an issue in the repository.