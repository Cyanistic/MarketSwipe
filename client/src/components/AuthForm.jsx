import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate, Link } from 'react-router-dom'; // Use React Router for navigation
import './AuthForm.css';
import { BASE_URL } from '../App';

const AuthForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate(); // Hook to navigate to different pages

  const handleLoginSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Reset error on each submission

    try {
      // Post the login details to the auth route
      const response = await axios.post(`${BASE_URL}/api/auth/login`, { email, password });

      if (response.status === 200) {
        // On successful login, store the JWT token in localStorage
        const token = response.headers['authorization']; // Get token from response header

        if (token) {
          localStorage.setItem('token', token.replace('Bearer ', ''));
        }
        
        navigate('/shopping', { state: { userId: response.data.id, email: response.data.email } });
      }
    } catch (err) {
      // Handle errors
      setError(err.response?.data?.message || 'Invalid credentials or something went wrong!');
    }
  };

  return (
    <form className='auth-form' onSubmit={handleLoginSubmit}>
        <div className='input-group'>
            <label>Email:</label>
            <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
        </div>

        <div className='input-group'>
            <label>Password:</label>
            <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
        </div>

        {error && <div className='error'>{error}</div>}

        <div className='center'>
            <button type="submit">Login</button>
        </div>

        <div className='link'>
            <Link to="/new">Create Account</Link> {/* Link to create user page */}
        </div>
    </form>
  );
};

export default AuthForm;
