from scapy.all import rdpcap, IP, TCP, UDP, DNS, ICMP, ARP
import pandas as pd
from collections import defaultdict, Counter
import time
from datetime import datetime

class PcapAnalyzer:
    def __init__(self):
        self.packets = []
        self.analysis_results = {}
    
    def analyze_pcap(self, filepath):
        """Main analysis function for PCAP files"""
        try:
            print(f"Loading PCAP file: {filepath}")
            self.packets = rdpcap(filepath)
            print(f"Loaded {len(self.packets)} packets")
            
            # Perform various analyses
            basic_stats = self._get_basic_statistics()
            protocol_dist = self._get_protocol_distribution()
            ip_conversations = self._get_ip_conversations()
            tcp_analysis = self._get_tcp_analysis()
            dns_analysis = self._get_dns_analysis()
            anomalies = self._detect_anomalies()
            timeline = self._get_traffic_timeline()
            
            self.analysis_results = {
                'basic_stats': basic_stats,
                'protocol_distribution': protocol_dist,
                'ip_conversations': ip_conversations,
                'tcp_analysis': tcp_analysis,
                'dns_analysis': dns_analysis,
                'anomalies': anomalies,
                'timeline': timeline,
                'total_packets': len(self.packets)
            }
            
            return self.analysis_results
            
        except Exception as e:
            raise Exception(f"PCAP analysis failed: {str(e)}")
    
    def _get_basic_statistics(self):
        """Calculate basic packet statistics"""
        if not self.packets:
            return {}
        
        total_packets = len(self.packets)
        total_bytes = sum(len(pkt) for pkt in self.packets)
        
        # Time analysis
        timestamps = [float(pkt.time) for pkt in self.packets if hasattr(pkt, 'time')]
        if timestamps:
            duration = max(timestamps) - min(timestamps)
            start_time = datetime.fromtimestamp(min(timestamps))
            end_time = datetime.fromtimestamp(max(timestamps))
        else:
            duration = 0
            start_time = end_time = datetime.now()
        
        # Calculate throughput
        throughput_bps = total_bytes / duration if duration > 0 else 0
        throughput_pps = total_packets / duration if duration > 0 else 0
        
        return {
            'total_packets': total_packets,
            'total_bytes': total_bytes,
            'duration_seconds': round(duration, 2),
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'throughput_bps': round(throughput_bps, 2),
            'throughput_pps': round(throughput_pps, 2),
            'avg_packet_size': round(total_bytes / total_packets, 2) if total_packets > 0 else 0
        }
    
    def _get_protocol_distribution(self):
        """Analyze protocol distribution"""
        protocol_counts = Counter()
        
        for pkt in self.packets:
            if IP in pkt:
                if TCP in pkt:
                    protocol_counts['TCP'] += 1
                elif UDP in pkt:
                    protocol_counts['UDP'] += 1
                elif ICMP in pkt:
                    protocol_counts['ICMP'] += 1
                else:
                    protocol_counts['Other IP'] += 1
            elif ARP in pkt:
                protocol_counts['ARP'] += 1
            else:
                protocol_counts['Other'] += 1
        
        # Convert to percentage
        total = sum(protocol_counts.values())
        protocol_percentages = {
            proto: {'count': count, 'percentage': round((count / total) * 100, 2)}
            for proto, count in protocol_counts.items()
        }
        
        return protocol_percentages
    
    def _get_ip_conversations(self):
        """Analyze IP conversations"""
        conversations = defaultdict(lambda: {'packets': 0, 'bytes': 0})
        
        for pkt in self.packets:
            if IP in pkt:
                src_ip = pkt[IP].src
                dst_ip = pkt[IP].dst
                conversation = tuple(sorted([src_ip, dst_ip]))
                
                conversations[conversation]['packets'] += 1
                conversations[conversation]['bytes'] += len(pkt)
        
        # Sort by packet count and return top 10
        sorted_conversations = sorted(
            conversations.items(),
            key=lambda x: x[1]['packets'],
            reverse=True
        )[:10]
        
        return [
            {
                'endpoints': f"{conv[0]} ↔ {conv[1]}",
                'packets': data['packets'],
                'bytes': data['bytes']
            }
            for conv, data in sorted_conversations
        ]
    
    def _get_tcp_analysis(self):
        """Analyze TCP connections and streams"""
        tcp_packets = [pkt for pkt in self.packets if TCP in pkt and IP in pkt]
        
        if not tcp_packets:
            return {'total_connections': 0, 'success_rate': 0, 'failed_connections': 0}
        
        # Track TCP connections
        connections = defaultdict(lambda: {'syn': 0, 'syn_ack': 0, 'ack': 0, 'fin': 0, 'rst': 0})
        
        for pkt in tcp_packets:
            src_ip = pkt[IP].src
            dst_ip = pkt[IP].dst
            src_port = pkt[TCP].sport
            dst_port = pkt[TCP].dport
            
            connection_key = (src_ip, src_port, dst_ip, dst_port)
            
            flags = pkt[TCP].flags
            if flags & 0x02:  # SYN
                connections[connection_key]['syn'] += 1
            if flags & 0x12:  # SYN-ACK
                connections[connection_key]['syn_ack'] += 1
            if flags & 0x10:  # ACK
                connections[connection_key]['ack'] += 1
            if flags & 0x01:  # FIN
                connections[connection_key]['fin'] += 1
            if flags & 0x04:  # RST
                connections[connection_key]['rst'] += 1
        
        # Calculate success rate
        successful_connections = sum(1 for conn in connections.values() 
                                   if conn['syn'] > 0 and conn['syn_ack'] > 0)
        total_connection_attempts = sum(1 for conn in connections.values() if conn['syn'] > 0)
        
        success_rate = (successful_connections / total_connection_attempts * 100) if total_connection_attempts > 0 else 0
        
        return {
            'total_connections': len(connections),
            'successful_connections': successful_connections,
            'failed_connections': total_connection_attempts - successful_connections,
            'success_rate': round(success_rate, 2),
            'total_tcp_packets': len(tcp_packets)
        }
    
    def _get_dns_analysis(self):
        """Analyze DNS traffic"""
        dns_packets = [pkt for pkt in self.packets if DNS in pkt]
        
        if not dns_packets:
            return {'total_queries': 0, 'total_responses': 0, 'top_domains': []}
        
        queries = []
        responses = []
        domains = Counter()
        
        for pkt in dns_packets:
            dns_layer = pkt[DNS]
            if dns_layer.qr == 0:  # Query
                queries.append(pkt)
                if dns_layer.qd:
                    domain = dns_layer.qd.qname.decode('utf-8').rstrip('.')
                    domains[domain] += 1
            else:  # Response
                responses.append(pkt)
        
        top_domains = [{'domain': domain, 'count': count} 
                      for domain, count in domains.most_common(10)]
        
        return {
            'total_queries': len(queries),
            'total_responses': len(responses),
            'top_domains': top_domains,
            'unique_domains': len(domains)
        }
    
    def _detect_anomalies(self):
        """Detect potential network anomalies"""
        anomalies = []
        
        # Port scan detection
        port_scan_threshold = 10
        src_ports = defaultdict(set)
        
        for pkt in self.packets:
            if TCP in pkt and IP in pkt:
                src_ip = pkt[IP].src
                dst_port = pkt[TCP].dport
                src_ports[src_ip].add(dst_port)
        
        for src_ip, ports in src_ports.items():
            if len(ports) > port_scan_threshold:
                anomalies.append({
                    'type': 'Potential Port Scan',
                    'description': f'IP {src_ip} accessed {len(ports)} different ports',
                    'severity': 'Medium',
                    'source_ip': src_ip
                })
        
        # High frequency traffic detection
        ip_packet_counts = Counter()
        for pkt in self.packets:
            if IP in pkt:
                ip_packet_counts[pkt[IP].src] += 1
        
        # Flag IPs with unusually high packet counts - only if we have IP packets
        if ip_packet_counts:
            avg_packets = sum(ip_packet_counts.values()) / len(ip_packet_counts)
            threshold = avg_packets * 5  # 5x average
            
            for ip, count in ip_packet_counts.items():
                if count > threshold:
                    anomalies.append({
                        'type': 'High Frequency Traffic',
                        'description': f'IP {ip} generated {count} packets (avg: {avg_packets:.1f})',
                        'severity': 'Low',
                        'source_ip': ip
                    })
        
        return anomalies
    
    def _get_traffic_timeline(self):
        """Generate traffic timeline data"""
        if not self.packets:
            return []
        
        # Group packets by time intervals (1-second buckets)
        timeline_data = defaultdict(lambda: {'packets': 0, 'bytes': 0})
        
        for pkt in self.packets:
            if hasattr(pkt, 'time'):
                timestamp = int(float(pkt.time))
                timeline_data[timestamp]['packets'] += 1
                timeline_data[timestamp]['bytes'] += len(pkt)
        
        # Convert to list format for frontend
        timeline = []
        for timestamp in sorted(timeline_data.keys()):
            timeline.append({
                'timestamp': timestamp,
                'datetime': datetime.fromtimestamp(timestamp).isoformat(),
                'packets': timeline_data[timestamp]['packets'],
                'bytes': timeline_data[timestamp]['bytes']
            })
        
        return timeline
    
    def filter_by_protocol(self, analysis_data, protocol):
        """Filter analysis data by specific protocol"""
        if protocol not in ['TCP', 'UDP', 'DNS', 'HTTP', 'ICMP']:
            raise ValueError(f"Unsupported protocol: {protocol}")
        
        filtered_packets = []
        
        for pkt in self.packets:
            if protocol == 'TCP' and TCP in pkt:
                filtered_packets.append(pkt)
            elif protocol == 'UDP' and UDP in pkt:
                filtered_packets.append(pkt)
            elif protocol == 'DNS' and DNS in pkt:
                filtered_packets.append(pkt)
            elif protocol == 'ICMP' and ICMP in pkt:
                filtered_packets.append(pkt)
            elif protocol == 'HTTP' and TCP in pkt and (pkt[TCP].dport == 80 or pkt[TCP].sport == 80):
                filtered_packets.append(pkt)
        
        # Temporarily store original packets and analyze filtered set
        original_packets = self.packets
        self.packets = filtered_packets
        
        try:
            filtered_analysis = {
                'protocol': protocol,
                'filtered_packet_count': len(filtered_packets),
                'basic_stats': self._get_basic_statistics(),
                'ip_conversations': self._get_ip_conversations(),
                'timeline': self._get_traffic_timeline()
            }
        finally:
            # Restore original packets
            self.packets = original_packets
        
        return filtered_analysis