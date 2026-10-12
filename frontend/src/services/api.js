import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getHealth = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};

export const getDashboardSummary = async () => {
  const response = await apiClient.get('/api/dashboard/summary');
  return response.data;
};

export const createPrediction = async (payload) => {
  const response = await apiClient.post('/api/predictions', payload);
  return response.data;
};

export const getPredictionHistory = async (limit = 50) => {
  const response = await apiClient.get(`/api/history?limit=${limit}`);
  return response.data;
};

export const getHistoricalData = async (params = {}) => {
  const response = await apiClient.get('/api/historical-data', { params });
  return response.data;
};

export const getModelInfo = async () => {
  const response = await apiClient.get('/api/model-info');
  return response.data;
};

export default apiClient;
