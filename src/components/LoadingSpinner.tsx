import React from 'react';
import { Loader2 } from 'lucide-react';

const LoadingSpinner: React.FC = () => {
  return (
    <div className="flex flex-col items-center space-y-4">
      <div className="relative">
        <div className="w-12 h-12 border-4 border-slate-600 rounded-full animate-spin"></div>
        <div className="absolute top-0 left-0 w-12 h-12 border-4 border-transparent border-t-blue-500 rounded-full animate-spin"></div>
      </div>
      <div className="text-center">
        <p className="text-white font-medium">Analyzing PCAP file...</p>
        <p className="text-slate-400 text-sm">This may take a few moments</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;