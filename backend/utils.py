from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import csv
from datetime import datetime
import json

def generate_pdf_report(analysis_data, filename):
    """Generate PDF report from analysis data"""
    buffer = io.BytesIO()
    
    # Create PDF document
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    story.append(Paragraph("OGPW Network Traffic Analysis Report", title_style))
    story.append(Spacer(1, 20))
    
    # File information
    story.append(Paragraph(f"<b>Analyzed File:</b> {filename}", styles['Normal']))
    story.append(Paragraph(f"<b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Basic Statistics
    if 'basic_stats' in analysis_data:
        story.append(Paragraph("Basic Statistics", styles['Heading2']))
        stats = analysis_data['basic_stats']
        
        stats_data = [
            ['Metric', 'Value'],
            ['Total Packets', f"{stats.get('total_packets', 'N/A'):,}"],
            ['Total Bytes', f"{stats.get('total_bytes', 'N/A'):,}"],
            ['Duration (seconds)', f"{stats.get('duration_seconds', 'N/A')}"],
            ['Average Packet Size', f"{stats.get('avg_packet_size', 'N/A')} bytes"],
            ['Throughput (packets/sec)', f"{stats.get('throughput_pps', 'N/A')}"],
            ['Throughput (bytes/sec)', f"{stats.get('throughput_bps', 'N/A'):,}"]
        ]
        
        stats_table = Table(stats_data)
        stats_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(stats_table)
        story.append(Spacer(1, 20))
    
    # Protocol Distribution
    if 'protocol_distribution' in analysis_data:
        story.append(Paragraph("Protocol Distribution", styles['Heading2']))
        protocols = analysis_data['protocol_distribution']
        
        protocol_data = [['Protocol', 'Packets', 'Percentage']]
        for proto, data in protocols.items():
            protocol_data.append([
                proto,
                f"{data.get('count', 0):,}",
                f"{data.get('percentage', 0)}%"
            ])
        
        protocol_table = Table(protocol_data)
        protocol_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(protocol_table)
        story.append(Spacer(1, 20))
    
    # TCP Analysis
    if 'tcp_analysis' in analysis_data:
        story.append(Paragraph("TCP Connection Analysis", styles['Heading2']))
        tcp = analysis_data['tcp_analysis']
        
        tcp_data = [
            ['Metric', 'Value'],
            ['Total Connections', f"{tcp.get('total_connections', 'N/A'):,}"],
            ['Successful Connections', f"{tcp.get('successful_connections', 'N/A'):,}"],
            ['Failed Connections', f"{tcp.get('failed_connections', 'N/A'):,}"],
            ['Success Rate', f"{tcp.get('success_rate', 'N/A')}%"],
            ['Total TCP Packets', f"{tcp.get('total_tcp_packets', 'N/A'):,}"]
        ]
        
        tcp_table = Table(tcp_data)
        tcp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(tcp_table)
        story.append(Spacer(1, 20))
    
    # Anomalies
    if 'anomalies' in analysis_data and analysis_data['anomalies']:
        story.append(Paragraph("Security Anomalies", styles['Heading2']))
        anomalies = analysis_data['anomalies']
        
        for anomaly in anomalies:
            story.append(Paragraph(f"<b>{anomaly.get('type', 'Unknown Anomaly')}</b>", styles['Normal']))
            story.append(Paragraph(f"Description: {anomaly.get('description', 'No description')}", styles['Normal']))
            story.append(Paragraph(f"Severity: {anomaly.get('severity', 'Unknown')}", styles['Normal']))
            if 'source_ip' in anomaly:
                story.append(Paragraph(f"Source IP: {anomaly['source_ip']}", styles['Normal']))
            story.append(Spacer(1, 10))
    
    # Top IP Conversations
    if 'ip_conversations' in analysis_data:
        story.append(Paragraph("Top IP Conversations", styles['Heading2']))
        conversations = analysis_data['ip_conversations']
        
        if conversations:
            conv_data = [['Endpoints', 'Packets', 'Bytes']]
            for conv in conversations[:10]:  # Top 10
                conv_data.append([
                    conv.get('endpoints', 'Unknown'),
                    f"{conv.get('packets', 0):,}",
                    f"{conv.get('bytes', 0):,}"
                ])
            
            conv_table = Table(conv_data)
            conv_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(conv_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def generate_csv_report(analysis_data, filename):
    """Generate CSV report from analysis data"""
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    
    # Header
    writer.writerow(['OGPW Network Traffic Analysis Report'])
    writer.writerow(['Analyzed File:', filename])
    writer.writerow(['Report Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    writer.writerow([])  # Empty row
    
    # Basic Statistics
    if 'basic_stats' in analysis_data:
        writer.writerow(['Basic Statistics'])
        stats = analysis_data['basic_stats']
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Packets', stats.get('total_packets', 'N/A')])
        writer.writerow(['Total Bytes', stats.get('total_bytes', 'N/A')])
        writer.writerow(['Duration (seconds)', stats.get('duration_seconds', 'N/A')])
        writer.writerow(['Average Packet Size', f"{stats.get('avg_packet_size', 'N/A')} bytes"])
        writer.writerow(['Throughput (packets/sec)', stats.get('throughput_pps', 'N/A')])
        writer.writerow(['Throughput (bytes/sec)', stats.get('throughput_bps', 'N/A')])
        writer.writerow([])  # Empty row
    
    # Protocol Distribution
    if 'protocol_distribution' in analysis_data:
        writer.writerow(['Protocol Distribution'])
        writer.writerow(['Protocol', 'Packets', 'Percentage'])
        protocols = analysis_data['protocol_distribution']
        for proto, data in protocols.items():
            writer.writerow([proto, data.get('count', 0), f"{data.get('percentage', 0)}%"])
        writer.writerow([])  # Empty row
    
    # TCP Analysis
    if 'tcp_analysis' in analysis_data:
        writer.writerow(['TCP Connection Analysis'])
        tcp = analysis_data['tcp_analysis']
        writer.writerow(['Metric', 'Value'])
        writer.writerow(['Total Connections', tcp.get('total_connections', 'N/A')])
        writer.writerow(['Successful Connections', tcp.get('successful_connections', 'N/A')])
        writer.writerow(['Failed Connections', tcp.get('failed_connections', 'N/A')])
        writer.writerow(['Success Rate', f"{tcp.get('success_rate', 'N/A')}%"])
        writer.writerow(['Total TCP Packets', tcp.get('total_tcp_packets', 'N/A')])
        writer.writerow([])  # Empty row
    
    # DNS Analysis
    if 'dns_analysis' in analysis_data:
        writer.writerow(['DNS Analysis'])
        dns = analysis_data['dns_analysis']
        writer.writerow(['Total DNS Queries', dns.get('total_queries', 'N/A')])
        writer.writerow(['Total DNS Responses', dns.get('total_responses', 'N/A')])
        writer.writerow(['Unique Domains', dns.get('unique_domains', 'N/A')])
        writer.writerow([])
        
        if 'top_domains' in dns and dns['top_domains']:
            writer.writerow(['Top Queried Domains'])
            writer.writerow(['Domain', 'Query Count'])
            for domain_info in dns['top_domains']:
                writer.writerow([domain_info.get('domain', 'Unknown'), domain_info.get('count', 0)])
            writer.writerow([])
    
    # Anomalies
    if 'anomalies' in analysis_data and analysis_data['anomalies']:
        writer.writerow(['Security Anomalies'])
        writer.writerow(['Type', 'Description', 'Severity', 'Source IP'])
        for anomaly in analysis_data['anomalies']:
            writer.writerow([
                anomaly.get('type', 'Unknown'),
                anomaly.get('description', 'No description'),
                anomaly.get('severity', 'Unknown'),
                anomaly.get('source_ip', 'N/A')
            ])
        writer.writerow([])
    
    # IP Conversations
    if 'ip_conversations' in analysis_data:
        writer.writerow(['Top IP Conversations'])
        writer.writerow(['Endpoints', 'Packets', 'Bytes'])
        conversations = analysis_data['ip_conversations']
        for conv in conversations:
            writer.writerow([
                conv.get('endpoints', 'Unknown'),
                conv.get('packets', 0),
                conv.get('bytes', 0)
            ])
    
    # Convert StringIO to BytesIO for file response
    csv_content = buffer.getvalue()
    buffer.close()
    
    bytes_buffer = io.BytesIO()
    bytes_buffer.write(csv_content.encode('utf-8'))
    bytes_buffer.seek(0)
    
    return bytes_buffer