// src/pages/RegisterPage.js
import React, { useState } from 'react';
import axios from '../api/axios';

const RegisterPage = () => {
  const [formData, setFormData] = useState({ email: '', password: '', role: 'user' });
  const [message, setMessage] = useState('');

  const handleChange = e =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await axios.post('/auth/register', formData);
      setMessage(res.data.message || 'User registered successfully');
      setFormData({ email: '', password: '', role: 'user' });
    } catch (err) {
      setMessage('Registration failed');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Register</h2>
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

export default RegisterPage;
