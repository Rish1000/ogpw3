import React, { useState, useEffect } from 'react';
import { Upload, MessageCircle, BarChart3, Shield, Network, Download, Filter } from 'lucide-react';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import Dashboard from './components/Dashboard';
import ProtocolFilter from './components/ProtocolFilter';
import LoadingSpinner from './components/LoadingSpinner';
import * as api from './services/api';

interface AnalysisData {
  basic_stats?: any;
  protocol_distribution?: any;
  ip_conversations?: any;
  tcp_streams?: any;
  dns_analysis?: any;
  anomalies?: any;
  kpis?: any;
  timeline?: any;
}

function App() {
  const [currentView, setCurrentView] = useState<'upload' | 'dashboard' | 'chat' | 'filter'>('upload');
  const [analysisData, setAnalysisData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentFileName, setCurrentFileName] = useState<string>('');

  const handleFileUpload = async (file: File) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.uploadPcapFile(file);
      setAnalysisData(result.analysis);
      setCurrentFileName(result.filename);
      setCurrentView('dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
    } finally {
      setLoading(false);
    }
  };

  const handleExportPDF = async () => {
    try {
      await api.exportPDF();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Export failed');
    }
  };

  const handleExportCSV = async () => {
    try {
      await api.exportCSV();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Export failed');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Navigation Header */}
      <nav className="bg-slate-800/50 backdrop-blur-sm border-b border-slate-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-600 rounded-lg">
                <Shield className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">OGPW</h1>
                <p className="text-xs text-slate-400">AI-Powered Network Traffic Analysis</p>
              </div>
            </div>
            
            {analysisData && (
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleExportPDF}
                  className="flex items-center space-x-2 px-3 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors"
                >
                  <Download className="h-4 w-4" />
                  <span className="hidden sm:inline">PDF</span>
                </button>
                <button
                  onClick={handleExportCSV}
                  className="flex items-center space-x-2 px-3 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
                >
                  <Download className="h-4 w-4" />
                  <span className="hidden sm:inline">CSV</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="flex h-[calc(100vh-4rem)]">
        {/* Sidebar */}
        {analysisData && (
          <div className="w-64 bg-slate-800/30 backdrop-blur-sm border-r border-slate-700/50 p-4">
            <div className="mb-6">
              <h3 className="text-sm font-medium text-slate-400 mb-2">CURRENT FILE</h3>
              <p className="text-white text-sm truncate" title={currentFileName}>
                {currentFileName}
              </p>
            </div>
            
            <nav className="space-y-2">
              <button
                onClick={() => setCurrentView('dashboard')}
                className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                  currentView === 'dashboard' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'
                }`}
              >
                <BarChart3 className="h-5 w-5" />
                <span>Dashboard</span>
              </button>
              
              <button
                onClick={() => setCurrentView('chat')}
                className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                  currentView === 'chat' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'
                }`}
              >
                <MessageCircle className="h-5 w-5" />
                <span>AI Assistant</span>
              </button>
              
              <button
                onClick={() => setCurrentView('filter')}
                className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                  currentView === 'filter' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'
                }`}
              >
                <Filter className="h-5 w-5" />
                <span>Protocol Filter</span>
              </button>
              
              <button
                onClick={() => setCurrentView('upload')}
                className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg transition-colors ${
                  currentView === 'upload' 
                    ? 'bg-blue-600 text-white' 
                    : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'
                }`}
              >
                <Upload className="h-5 w-5" />
                <span>Upload New</span>
              </button>
            </nav>
          </div>
        )}

        {/* Main Content Area */}
        <div className="flex-1 p-6 overflow-auto">
          {error && (
            <div className="mb-6 bg-red-900/20 border border-red-500/50 text-red-300 px-4 py-3 rounded-lg">
              <p className="font-medium">Error</p>
              <p className="text-sm">{error}</p>
            </div>
          )}

          {loading && (
            <div className="flex items-center justify-center h-64">
              <LoadingSpinner />
            </div>
          )}

          {!loading && (
            <>
              {currentView === 'upload' && (
                <div className="max-w-2xl mx-auto">
                  <div className="text-center mb-8">
                    <Network className="h-16 w-16 text-blue-400 mx-auto mb-4" />
                    <h2 className="text-3xl font-bold text-white mb-2">
                      OGPW Network Analysis
                    </h2>
                    <p className="text-slate-400">
                      Upload your PCAP files for AI-powered security analysis
                    </p>
                  </div>
                  <FileUpload onFileUpload={handleFileUpload} />
                </div>
              )}

              {currentView === 'dashboard' && analysisData && (
                <Dashboard data={analysisData} />
              )}

              {currentView === 'chat' && analysisData && (
                <ChatInterface />
              )}

              {currentView === 'filter' && analysisData && (
                <ProtocolFilter />
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;