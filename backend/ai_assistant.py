import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import openai
    openai.api_key = os.getenv('OPENAI_API_KEY')
    OPENAI_AVAILABLE = bool(openai.api_key)
except ImportError:
    OPENAI_AVAILABLE = False

class AIAssistant:
    def __init__(self):
        self.openai_available = OPENAI_AVAILABLE
        
    def process_query(self, user_message, analysis_data):
        """Process user query about network analysis data"""
        
        if self.openai_available:
            return self._process_with_openai(user_message, analysis_data)
        else:
            return self._process_with_fallback(user_message, analysis_data)
    
    def _process_with_openai(self, user_message, analysis_data):
        """Process query using OpenAI API"""
        try:
            # Prepare context from analysis data
            context = self._prepare_context(analysis_data)
            
            system_prompt = """You are a cybersecurity expert assistant analyzing network traffic data. 
            You have access to PCAP analysis results and can answer questions about network security, 
            traffic patterns, anomalies, and protocol analysis. Provide clear, technical but accessible 
            explanations based on the provided data."""
            
            user_prompt = f"""
            Network Analysis Data:
            {context}
            
            User Question: {user_message}
            
            Please provide a detailed analysis based on the network data above.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"AI processing error: {str(e)}. Falling back to pattern matching."
    
    def _process_with_fallback(self, user_message, analysis_data):
        """Process query using pattern matching fallback"""
        message_lower = user_message.lower()
        
        # Basic statistics queries
        if any(word in message_lower for word in ['packets', 'total', 'count', 'how many']):
            basic_stats = analysis_data.get('basic_stats', {})
            return f"""Based on the analysis:
            
• Total packets: {basic_stats.get('total_packets', 'N/A')}
• Total bytes: {basic_stats.get('total_bytes', 'N/A')}
• Duration: {basic_stats.get('duration_seconds', 'N/A')} seconds
• Average packet size: {basic_stats.get('avg_packet_size', 'N/A')} bytes
• Throughput: {basic_stats.get('throughput_pps', 'N/A')} packets/sec"""
        
        # Protocol distribution queries
        elif any(word in message_lower for word in ['protocol', 'tcp', 'udp', 'dns', 'distribution']):
            protocols = analysis_data.get('protocol_distribution', {})
            protocol_summary = []
            for proto, data in protocols.items():
                protocol_summary.append(f"• {proto}: {data.get('count', 0)} packets ({data.get('percentage', 0)}%)")
            
            return f"""Protocol Distribution:
            
{chr(10).join(protocol_summary)}"""
        
        # Anomaly queries
        elif any(word in message_lower for word in ['anomaly', 'suspicious', 'threat', 'attack', 'security']):
            anomalies = analysis_data.get('anomalies', [])
            if not anomalies:
                return "No significant anomalies detected in the network traffic."
            
            anomaly_summary = []
            for anomaly in anomalies:
                anomaly_summary.append(f"• {anomaly.get('type', 'Unknown')}: {anomaly.get('description', 'No description')}")
            
            return f"""Security Analysis - Detected Anomalies:
            
{chr(10).join(anomaly_summary)}
            
Recommendation: Review these findings and investigate any suspicious activities."""
        
        # TCP analysis queries
        elif any(word in message_lower for word in ['tcp', 'connection', 'success rate']):
            tcp_data = analysis_data.get('tcp_analysis', {})
            return f"""TCP Connection Analysis:
            
• Total connections: {tcp_data.get('total_connections', 'N/A')}
• Successful connections: {tcp_data.get('successful_connections', 'N/A')}
• Failed connections: {tcp_data.get('failed_connections', 'N/A')}
• Success rate: {tcp_data.get('success_rate', 'N/A')}%
• Total TCP packets: {tcp_data.get('total_tcp_packets', 'N/A')}"""
        
        # DNS analysis queries
        elif any(word in message_lower for word in ['dns', 'domain', 'query', 'resolution']):
            dns_data = analysis_data.get('dns_analysis', {})
            top_domains = dns_data.get('top_domains', [])
            
            domain_list = []
            for domain_info in top_domains[:5]:  # Top 5 domains
                domain_list.append(f"• {domain_info.get('domain', 'Unknown')}: {domain_info.get('count', 0)} queries")
            
            return f"""DNS Traffic Analysis:
            
• Total DNS queries: {dns_data.get('total_queries', 'N/A')}
• Total DNS responses: {dns_data.get('total_responses', 'N/A')}
• Unique domains: {dns_data.get('unique_domains', 'N/A')}

Top Queried Domains:
{chr(10).join(domain_list) if domain_list else '• No domain data available'}"""
        
        # IP conversation queries
        elif any(word in message_lower for word in ['ip', 'conversation', 'communication', 'traffic']):
            conversations = analysis_data.get('ip_conversations', [])
            conv_summary = []
            for conv in conversations[:5]:  # Top 5 conversations
                conv_summary.append(f"• {conv.get('endpoints', 'Unknown')}: {conv.get('packets', 0)} packets")
            
            return f"""Top IP Conversations:
            
{chr(10).join(conv_summary) if conv_summary else '• No conversation data available'}"""
        
        # General help
        elif any(word in message_lower for word in ['help', 'what can', 'capabilities']):
            return """I can help you analyze network traffic data. You can ask me about:

• Packet statistics and counts
• Protocol distribution (TCP, UDP, DNS, etc.)
• Security anomalies and threats
• TCP connection analysis
• DNS traffic patterns
• IP conversations and communications
• Traffic timeline and patterns

Try asking questions like:
- "How many packets were captured?"
- "What protocols were used?"
- "Are there any security threats?"
- "Show me TCP connection statistics"
- "What domains were queried?"
"""
        
        # Default response
        else:
            return """I can analyze your network traffic data. Try asking about:
            
• Packet counts and statistics
• Protocol distribution
• Security anomalies
• TCP connections
• DNS queries
• IP conversations

For example: "How many packets were captured?" or "Are there any security threats?"
"""
    
    def _prepare_context(self, analysis_data):
        """Prepare analysis data context for OpenAI"""
        context_parts = []
        
        # Basic statistics
        if 'basic_stats' in analysis_data:
            stats = analysis_data['basic_stats']
            context_parts.append(f"Basic Statistics: {json.dumps(stats, indent=2)}")
        
        # Protocol distribution
        if 'protocol_distribution' in analysis_data:
            protocols = analysis_data['protocol_distribution']
            context_parts.append(f"Protocol Distribution: {json.dumps(protocols, indent=2)}")
        
        # Anomalies
        if 'anomalies' in analysis_data:
            anomalies = analysis_data['anomalies']
            context_parts.append(f"Detected Anomalies: {json.dumps(anomalies, indent=2)}")
        
        # TCP analysis
        if 'tcp_analysis' in analysis_data:
            tcp = analysis_data['tcp_analysis']
            context_parts.append(f"TCP Analysis: {json.dumps(tcp, indent=2)}")
        
        # DNS analysis
        if 'dns_analysis' in analysis_data:
            dns = analysis_data['dns_analysis']
            context_parts.append(f"DNS Analysis: {json.dumps(dns, indent=2)}")
        
        return "\n\n".join(context_parts)