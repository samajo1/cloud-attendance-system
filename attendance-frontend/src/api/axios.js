import axios from 'axios';

const baseURL =
  process.env.NODE_ENV === 'production'
    ? 'https://http://127.0.0.1:10000/api'
    : 'http://localhost:5000/api';

const instance = axios.create({ baseURL });

instance.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default instance;
