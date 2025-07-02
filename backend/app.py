from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
from werkzeug.utils import secure_filename
from pcap_analyzer import PcapAnalyzer
from ai_assistant import AIAssistant
from utils import generate_pdf_report, generate_csv_report
import json

app = Flask(__name__)
CORS(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB
ALLOWED_EXTENSIONS = {'pcap', 'pcapng'}

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global variables to store current analysis
current_analysis = None
current_filename = None

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'OGPW Backend API is running'})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    global current_analysis, current_filename
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only .pcap and .pcapng files are allowed'}), 400
    
    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Analyze the PCAP file
        analyzer = PcapAnalyzer()
        analysis_result = analyzer.analyze_pcap(filepath)
        
        current_analysis = analysis_result
        current_filename = filename
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'message': 'File uploaded and analyzed successfully',
            'filename': filename,
            'analysis': analysis_result
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@app.route('/api/analysis/current', methods=['GET'])
def get_current_analysis():
    if current_analysis is None:
        return jsonify({'error': 'No analysis data available'}), 404
    
    return jsonify({
        'filename': current_filename,
        'analysis': current_analysis
    })

@app.route('/api/analysis/filter', methods=['POST'])
def filter_analysis():
    if current_analysis is None:
        return jsonify({'error': 'No analysis data available'}), 404
    
    data = request.get_json()
    protocol = data.get('protocol', '').upper()
    
    if not protocol:
        return jsonify({'error': 'Protocol parameter is required'}), 400
    
    try:
        analyzer = PcapAnalyzer()
        filtered_data = analyzer.filter_by_protocol(current_analysis, protocol)
        return jsonify(filtered_data)
    except Exception as e:
        return jsonify({'error': f'Filtering failed: {str(e)}'}), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    if current_analysis is None:
        return jsonify({'error': 'No analysis data available for AI assistant'}), 404
    
    data = request.get_json()
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'Message is required'}), 400
    
    try:
        ai_assistant = AIAssistant()
        response = ai_assistant.process_query(message, current_analysis)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': f'AI processing failed: {str(e)}'}), 500

@app.route('/api/export/pdf', methods=['GET'])
def export_pdf():
    if current_analysis is None:
        return jsonify({'error': 'No analysis data available'}), 404
    
    try:
        pdf_buffer = generate_pdf_report(current_analysis, current_filename)
        
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=f'{current_filename}_analysis.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        return jsonify({'error': f'PDF generation failed: {str(e)}'}), 500

@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    if current_analysis is None:
        return jsonify({'error': 'No analysis data available'}), 404
    
    try:
        csv_buffer = generate_csv_report(current_analysis, current_filename)
        
        return send_file(
            csv_buffer,
            as_attachment=True,
            download_name=f'{current_filename}_analysis.csv',
            mimetype='text/csv'
        )
    except Exception as e:
        return jsonify({'error': f'CSV generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    print("Starting OGPW Backend API...")
    print("API will be available at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)