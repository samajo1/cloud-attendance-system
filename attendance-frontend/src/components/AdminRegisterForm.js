import React, { useState } from 'react';
import axios from '../api/axios';

const AdminRegisterForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    role: 'user',
  });

  const [message, setMessage] = useState('');

  const handleChange = e =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await axios.post('/auth/register', formData);
      setMessage(res.data.message || 'User registered!');
      setFormData({ email: '', password: '', role: 'user' });
    } catch (err) {
      setMessage('Error: ' + err.response?.data?.message || 'Failed');
    }
  };

  return (
    <form onSubmit={handleSubmit} style={{ marginTop: '1rem' }}>
      <h3>Register a New User</h3>
      <input type="email" name="email" placeholder="Email" value={formData.email} onChange={handleChange} required />
      <input type="password" name="password" placeholder="Password" value={formData.password} onChange={handleChange} required />
      <select name="role" value={formData.role} onChange={handleChange}>
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </select>
      <button type="submit">Register</button>
      <p>{message}</p>
    </form>
  );
};

export default AdminRegisterForm;
