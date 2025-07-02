import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 300000, // 5 minutes for large file uploads
});

// Add request interceptor for debugging
apiClient.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Add response interceptor for debugging
apiClient.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.status, error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const uploadPcapFile = async (file: File) => {
  try {
    console.log('Uploading file:', file.name, 'Size:', file.size, 'bytes');
    
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await apiClient.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    console.log('Upload successful:', response.data);
    return response.data;
  } catch (error) {
    console.error('Upload failed:', error);
    if (axios.isAxiosError(error)) {
      if (error.response) {
        // Server responded with error status
        throw new Error(error.response.data?.error || `Server error: ${error.response.status}`);
      } else if (error.request) {
        // Request was made but no response received
        throw new Error('No response from server. Make sure the backend is running on port 5000.');
      } else {
        // Something else happened
        throw new Error(`Request failed: ${error.message}`);
      }
    }
    throw error;
  }
};

export const chatWithAI = async (message: string) => {
  const response = await apiClient.post('/chat', { message });
  return response.data;
};

export const getCurrentAnalysis = async () => {
  const response = await apiClient.get('/analysis/current');
  return response.data;
};

export const filterPackets = async (protocol: string) => {
  const response = await apiClient.post('/analysis/filter', { protocol });
  return response.data;
};

export const exportPDF = async () => {
  const response = await apiClient.get('/export/pdf', {
    responseType: 'blob',
  });
  
  // Create download link
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.download = `ogpw_analysis_${new Date().toISOString().split('T')[0]}.pdf`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

export const exportCSV = async () => {
  const response = await apiClient.get('/export/csv', {
    responseType: 'blob',
  });
  
  // Create download link
  const url = window.URL.createObjectURL(new Blob([response.data]));
  const link = document.createElement('a');
  link.href = url;
  link.download = `ogpw_analysis_${new Date().toISOString().split('T')[0]}.csv`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
};

export const healthCheck = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};