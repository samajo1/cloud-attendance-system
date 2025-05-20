// src/pages/DashboardPage.js
import React, { useEffect, useState, useContext } from 'react';
import axios from '../api/axios';
import { AuthContext } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import AdminRegisterForm from '../components/AdminRegisterForm';

const DashboardPage = () => {
  const { logout } = useContext(AuthContext);
  const [role, setRole] = useState('');
  const [logs, setLogs] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
  const getRole = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.get('/auth/role', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setRole(res.data.role);
    } catch (err) {
      logout();
      navigate('/');
    }
  };

  getRole();
}, [logout, navigate]); // ✅ Include both here


  const handleGetLogs = () => {
    const endpoint = role === 'admin' ? '/attendance/logs/all' : `/attendance/logs/${getEmailFromToken()}`;
    axios.get(endpoint)
      .then(res => setLogs(res.data.logs))
      .catch(err => console.error(err));
  };

  const getEmailFromToken = () => {
    const token = localStorage.getItem('token');
    if (!token) return '';
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.sub || '';
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Welcome to the Dashboard</h2>
      <p>Role: {role}</p>

      <button onClick={() => axios.post('/attendance/check-in')}>Check In</button>
      <button onClick={() => axios.post('/attendance/check-out')}>Check Out</button>

      <button onClick={handleGetLogs}>
        {role === 'admin' ? 'View All Logs' : 'View My Logs'}
      </button>
      {/* 👇 Show admin-only registration form */}
      {role === 'admin' && <AdminRegisterForm />}

      <div>
        <h3>Attendance Logs</h3>
        <ul>
          {logs.map(log => (
            <li key={log.id}>
              {log.email} | In: {log.check_in?.toDate?.() || log.check_in} | Out: {log.check_out?.toDate?.() || log.check_out}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default DashboardPage;
