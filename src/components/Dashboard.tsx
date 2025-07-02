import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';
import { Activity, Network, Shield, Zap, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

interface DashboardProps {
  data: any;
}

const Dashboard: React.FC<DashboardProps> = ({ data }) => {
  const COLORS = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4'];

  // Prepare protocol distribution data for charts
  const protocolData = data.protocol_distribution ? 
    Object.entries(data.protocol_distribution).map(([protocol, info]: [string, any]) => ({
      name: protocol,
      value: info.count,
      percentage: info.percentage
    })) : [];

  // Prepare IP conversation data
  const ipConversationData = data.ip_conversations ? 
    data.ip_conversations.slice(0, 10).map((conv: any, index: number) => ({
      name: `${conv.ips[0]} ↔ ${conv.ips[1]}`,
      packets: conv.packets,
      bytes: conv.bytes
    })) : [];

  // Prepare timeline data
  const timelineData = data.timeline ? 
    data.timeline.map((point: any) => ({
      time: new Date(point.timestamp).toLocaleTimeString(),
      packets: point.packet_count
    })) : [];

  return (
    <div className="space-y-6">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Network Analysis Dashboard</h2>
        <p className="text-slate-400">Comprehensive overview of your network traffic</p>
      </div>

      {/* KPI Cards */}
      {data.basic_stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-blue-600 rounded-lg">
                <Activity className="h-6 w-6 text-white" />
              </div>
              <div>
                <p className="text-slate-400 text-sm">Total Packets</p>
                <p className="text-2xl font-bold text-white">{data.basic_stats.total_packets?.toLocaleString()}</p>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-green-600 rounded-lg">
                <Network className="h-6 w-6 text-white" />
              </div>
              <div>
                <p className="text-slate-400 text-sm">Total Bytes</p>
                <p className="text-2xl font-bold text-white">{(data.basic_stats.total_bytes / 1024 / 1024).toFixed(2)} MB</p>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-yellow-600 rounded-lg">
                <Zap className="h-6 w-6 text-white" />
              </div>
              <div>
                <p className="text-slate-400 text-sm">Duration</p>
                <p className="text-2xl font-bold text-white">{data.basic_stats.duration_seconds}s</p>
              </div>
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
            <div className="flex items-center space-x-3">
              <div className="p-3 bg-purple-600 rounded-lg">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <p className="text-slate-400 text-sm">Packets/Sec</p>
                <p className="text-2xl font-bold text-white">{data.basic_stats.packets_per_second}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Connection KPIs */}
      {data.kpis && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">TCP Established</p>
                <p className="text-2xl font-bold text-green-400">{data.kpis.tcp_established_connections}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-400" />
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">TCP Failed</p>
                <p className="text-2xl font-bold text-red-400">{data.kpis.tcp_failed_connections}</p>
              </div>
              <XCircle className="h-8 w-8 text-red-400" />
            </div>
          </div>

          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-slate-400 text-sm">Success Rate</p>
                <p className="text-2xl font-bold text-blue-400">{data.kpis.connection_success_rate}%</p>
              </div>
              <Activity className="h-8 w-8 text-blue-400" />
            </div>
          </div>
        </div>
      )}

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Protocol Distribution Pie Chart */}
        {protocolData.length > 0 && (
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
            <h3 className="text-xl font-bold text-white mb-4">Protocol Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={protocolData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percentage }) => `${name} (${percentage}%)`}
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {protocolData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* IP Conversations Bar Chart */}
        {ipConversationData.length > 0 && (
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
            <h3 className="text-xl font-bold text-white mb-4">Top IP Conversations</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={ipConversationData} layout="horizontal">
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis type="number" stroke="#9CA3AF" />
                <YAxis 
                  type="category" 
                  dataKey="name" 
                  stroke="#9CA3AF" 
                  width={150}
                  fontSize={12}
                />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: '#1F2937', 
                    border: '1px solid #374151',
                    borderRadius: '8px'
                  }}
                />
                <Bar dataKey="packets" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* Timeline Chart */}
      {timelineData.length > 0 && (
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
          <h3 className="text-xl font-bold text-white mb-4">Traffic Timeline</h3>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={timelineData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="time" stroke="#9CA3AF" />
              <YAxis stroke="#9CA3AF" />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: '#1F2937', 
                  border: '1px solid #374151',
                  borderRadius: '8px'
                }}
              />
              <Line type="monotone" dataKey="packets" stroke="#10B981" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

      {/* Anomalies Section */}
      {data.anomalies && data.anomalies.length > 0 && (
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
          <div className="flex items-center space-x-3 mb-4">
            <AlertTriangle className="h-6 w-6 text-yellow-400" />
            <h3 className="text-xl font-bold text-white">Detected Anomalies</h3>
          </div>
          <div className="space-y-3">
            {data.anomalies.map((anomaly: any, index: number) => (
              <div key={index} className="flex items-start space-x-3 p-4 bg-slate-700/50 rounded-lg">
                <div className={`p-2 rounded-full ${
                  anomaly.severity === 'High' ? 'bg-red-600' :
                  anomaly.severity === 'Medium' ? 'bg-yellow-600' : 'bg-blue-600'
                }`}>
                  <Shield className="h-4 w-4 text-white" />
                </div>
                <div className="flex-1">
                  <p className="text-white font-medium">{anomaly.type}</p>
                  <p className="text-slate-400 text-sm">{anomaly.description}</p>
                  <span className={`inline-block mt-2 px-2 py-1 text-xs rounded-full ${
                    anomaly.severity === 'High' ? 'bg-red-900/30 text-red-300' :
                    anomaly.severity === 'Medium' ? 'bg-yellow-900/30 text-yellow-300' : 'bg-blue-900/30 text-blue-300'
                  }`}>
                    {anomaly.severity} Severity
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TCP Streams Table */}
      {data.tcp_streams && data.tcp_streams.length > 0 && (
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
          <h3 className="text-xl font-bold text-white mb-4">Top TCP Streams</h3>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-slate-700">
                  <th className="text-left py-3 px-4 text-slate-400 font-medium">Endpoints</th>
                  <th className="text-left py-3 px-4 text-slate-400 font-medium">Packets</th>
                  <th className="text-left py-3 px-4 text-slate-400 font-medium">Bytes</th>
                  <th className="text-left py-3 px-4 text-slate-400 font-medium">Ports</th>
                </tr>
              </thead>
              <tbody>
                {data.tcp_streams.slice(0, 10).map((stream: any, index: number) => (
                  <tr key={index} className="border-b border-slate-700/50 hover:bg-slate-700/30">
                    <td className="py-3 px-4 text-white text-sm">{stream.endpoints.join(' ↔ ')}</td>
                    <td className="py-3 px-4 text-slate-300">{stream.packets}</td>
                    <td className="py-3 px-4 text-slate-300">{(stream.bytes / 1024).toFixed(1)} KB</td>
                    <td className="py-3 px-4 text-slate-300">{stream.ports.join(', ')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;