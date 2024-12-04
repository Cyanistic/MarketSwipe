import React, { useState } from 'react';
import axios from 'axios';
import { Link, useNavigate } from 'react-router-dom';
import './AuthForm.css';
import { BASE_URL } from '../App';

const NewAuthForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (!email.includes('@')) {
      setError('Please enter a valid email address');
      return;
    }

    try {
      const response = await axios.post(`${BASE_URL}/api/auth/register`, { email, password });
      if (response.status === 201) {
        alert('User successfully created!');
        navigate('/login');
      }
    } catch (err) {
      if (err.response) {
        setError(err.response?.data?.message || 'Something went wrong during registration!');
      } else if (err.request) {
        setError('No response from the server. Please check if the server is running.');
      } else {
        setError('Error in setting up request: ' + err.message);
      }
    }
  };

  return (
    <form className="auth-form" onSubmit={handleSubmit}>
      <div className="input-group">
        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="example@mail.com"
          required
        />
      </div>

      <div className="input-group">
        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Str0ngP4ssw0rd!"
          required
        />
      </div>

      <div className="input-group">
        <label>Confirm Password:</label>
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          placeholder="***************"
          required
        />
      </div>

      {error && <div className="error">{error}</div>}

      <div className="center">
        <button type="submit">Create Account</button>
      </div>

      <div className="link">
        <Link to="/login">Already have an account? Login</Link>
      </div>
    </form>
  );
};

export default NewAuthForm;
