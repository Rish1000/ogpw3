import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      console.log('File selected:', file.name, 'Size:', file.size, 'bytes');
      onFileUpload(file);
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.tcpdump.pcap': ['.pcap'],
      'application/pcapng': ['.pcapng'],
      'application/octet-stream': ['.pcap', '.pcapng']
    },
    maxFiles: 1,
    maxSize: 500 * 1024 * 1024 // 500MB
  });

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all duration-300 ${
          isDragActive 
            ? 'border-blue-400 bg-blue-500/10 scale-105' 
            : 'border-slate-600 hover:border-blue-500 hover:bg-slate-800/50'
        }`}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-4">
          <div className={`p-4 rounded-full ${isDragActive ? 'bg-blue-500/20' : 'bg-slate-700/50'}`}>
            <Upload className={`h-12 w-12 ${isDragActive ? 'text-blue-400' : 'text-slate-400'}`} />
          </div>
          
          {isDragActive ? (
            <div>
              <p className="text-xl font-semibold text-blue-400">Drop the PCAP file here</p>
              <p className="text-slate-400">Release to start analysis</p>
            </div>
          ) : (
            <div>
              <p className="text-xl font-semibold text-white mb-2">
                Upload PCAP File for Analysis
              </p>
              <p className="text-slate-400 mb-4">
                Drag and drop your .pcap or .pcapng file here, or click to browse
              </p>
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors">
                Choose File
              </button>
            </div>
          )}
        </div>
      </div>

      {/* File Requirements */}
      <div className="mt-6 bg-slate-800/50 backdrop-blur-sm rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <FileText className="h-5 w-5 text-blue-400 mt-0.5" />
          <div>
            <h4 className="text-white font-medium mb-2">File Requirements</h4>
            <ul className="text-sm text-slate-400 space-y-1">
              <li>• Supported formats: .pcap, .pcapng</li>
              <li>• Maximum file size: 500MB</li>
              <li>• Contains network packet data</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Troubleshooting Tips */}
      <div className="mt-4 bg-green-900/20 border border-green-500/50 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <CheckCircle className="h-5 w-5 text-green-400 mt-0.5" />
          <div>
            <h4 className="text-green-300 font-medium mb-2">Troubleshooting Tips</h4>
            <ul className="text-sm text-green-400 space-y-1">
              <li>• Make sure the backend server is running on port 5000</li>
              <li>• Check that your file is a valid PCAP format</li>
              <li>• Ensure file size is under 500MB</li>
              <li>• Try refreshing the page if upload fails</li>
            </ul>
          </div>
        </div>
      </div>

      {/* File Rejection Errors */}
      {fileRejections.length > 0 && (
        <div className="mt-4 bg-red-900/20 border border-red-500/50 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <AlertCircle className="h-5 w-5 text-red-400 mt-0.5" />
            <div>
              <h4 className="text-red-300 font-medium mb-2">Upload Error</h4>
              {fileRejections.map(({ file, errors }) => (
                <div key={file.name} className="text-sm text-red-400">
                  <p className="font-medium">{file.name}</p>
                  <ul className="list-disc list-inside ml-2">
                    {errors.map((error) => (
                      <li key={error.code}>{error.message}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUpload;