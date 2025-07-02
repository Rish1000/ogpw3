import React, { useState } from 'react';
import { Filter, Search } from 'lucide-react';
import * as api from '../services/api';
import LoadingSpinner from './LoadingSpinner';

const ProtocolFilter: React.FC = () => {
  const [selectedProtocol, setSelectedProtocol] = useState<string>('');
  const [filterResults, setFilterResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const protocols = [
    { value: 'TCP', label: 'TCP', description: 'Transmission Control Protocol' },
    { value: 'UDP', label: 'UDP', description: 'User Datagram Protocol' },
    { value: 'DNS', label: 'DNS', description: 'Domain Name System' },
    { value: 'HTTP', label: 'HTTP', description: 'HyperText Transfer Protocol' },
    { value: 'ICMP', label: 'ICMP', description: 'Internet Control Message Protocol' }
  ];

  const handleFilter = async () => {
    if (!selectedProtocol) return;

    setLoading(true);
    setError(null);

    try {
      const result = await api.filterPackets(selectedProtocol);
      setFilterResults(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Filter failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">Protocol Filter</h2>
        <p className="text-slate-400">Filter and analyze packets by specific protocols</p>
      </div>

      {/* Protocol Selection */}
      <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
        <h3 className="text-xl font-bold text-white mb-4">Select Protocol</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
          {protocols.map((protocol) => (
            <div
              key={protocol.value}
              onClick={() => setSelectedProtocol(protocol.value)}
              className={`p-4 rounded-lg border cursor-pointer transition-all ${
                selectedProtocol === protocol.value
                  ? 'border-blue-500 bg-blue-500/20'
                  : 'border-slate-600 hover:border-slate-500 hover:bg-slate-700/50'
              }`}
            >
              <div className="flex items-center space-x-3">
                <div className={`p-2 rounded-lg ${
                  selectedProtocol === protocol.value ? 'bg-blue-600' : 'bg-slate-600'
                }`}>
                  <Filter className="h-5 w-5 text-white" />
                </div>
                <div>
                  <h4 className="text-white font-medium">{protocol.label}</h4>
                  <p className="text-slate-400 text-sm">{protocol.description}</p>
                </div>
              </div>
            </div>
          ))}
        </div>

        <button
          onClick={handleFilter}
          disabled={!selectedProtocol || loading}
          className="flex items-center space-x-2 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 disabled:cursor-not-allowed text-white px-6 py-3 rounded-lg font-medium transition-colors"
        >
          {loading ? (
            <>
              <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
              <span>Filtering...</span>
            </>
          ) : (
            <>
              <Search className="h-5 w-5" />
              <span>Filter Packets</span>
            </>
          )}
        </button>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-900/20 border border-red-500/50 rounded-lg p-4">
          <p className="text-red-300 font-medium">Error</p>
          <p className="text-red-400 text-sm">{error}</p>
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="flex items-center justify-center py-12">
          <LoadingSpinner />
        </div>
      )}

      {/* Filter Results */}
      {filterResults && !loading && (
        <div className="space-y-6">
          {/* Basic Stats */}
          <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
            <h3 className="text-xl font-bold text-white mb-4">
              {filterResults.protocol} Protocol Analysis
            </h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-700/50 rounded-lg p-4">
                <p className="text-slate-400 text-sm">Filtered Packets</p>
                <p className="text-2xl font-bold text-white">{filterResults.packet_count?.toLocaleString()}</p>
              </div>
              
              {filterResults.basic_stats && (
                <>
                  <div className="bg-slate-700/50 rounded-lg p-4">
                    <p className="text-slate-400 text-sm">Total Bytes</p>
                    <p className="text-2xl font-bold text-white">
                      {((filterResults.basic_stats.total_bytes || 0) / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                  
                  <div className="bg-slate-700/50 rounded-lg p-4">
                    <p className="text-slate-400 text-sm">Duration</p>
                    <p className="text-2xl font-bold text-white">
                      {filterResults.basic_stats.duration_seconds || 0}s
                    </p>
                  </div>
                </>
              )}
            </div>
          </div>

          {/* IP Conversations for filtered protocol */}
          {filterResults.ip_conversations && filterResults.ip_conversations.length > 0 && (
            <div className="bg-slate-800/50 backdrop-blur-sm rounded-xl p-6 border border-slate-700/50">
              <h3 className="text-xl font-bold text-white mb-4">
                Top IP Conversations ({filterResults.protocol})
              </h3>
              
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="border-b border-slate-700">
                      <th className="text-left py-3 px-4 text-slate-400 font-medium">IP Addresses</th>
                      <th className="text-left py-3 px-4 text-slate-400 font-medium">Packets</th>
                      <th className="text-left py-3 px-4 text-slate-400 font-medium">Bytes</th>
                      <th className="text-left py-3 px-4 text-slate-400 font-medium">Data Transfer</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filterResults.ip_conversations.slice(0, 15).map((conv: any, index: number) => (
                      <tr key={index} className="border-b border-slate-700/50 hover:bg-slate-700/30">
                        <td className="py-3 px-4 text-white text-sm">
                          {conv.ips[0]} ↔ {conv.ips[1]}
                        </td>
                        <td className="py-3 px-4 text-slate-300">{conv.packets}</td>
                        <td className="py-3 px-4 text-slate-300">{(conv.bytes / 1024).toFixed(1)} KB</td>
                        <td className="py-3 px-4">
                          <div className="w-full bg-slate-700 rounded-full h-2">
                            <div 
                              className="bg-blue-600 h-2 rounded-full"
                              style={{ 
                                width: `${Math.min((conv.bytes / Math.max(...filterResults.ip_conversations.map((c: any) => c.bytes))) * 100, 100)}%` 
                              }}
                            ></div>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          {/* No results message */}
          {filterResults.error && (
            <div className="bg-yellow-900/20 border border-yellow-500/50 rounded-lg p-6 text-center">
              <p className="text-yellow-300 font-medium">{filterResults.error}</p>
              <p className="text-yellow-400 text-sm mt-2">
                Try selecting a different protocol or check if your PCAP file contains the selected protocol traffic.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ProtocolFilter;