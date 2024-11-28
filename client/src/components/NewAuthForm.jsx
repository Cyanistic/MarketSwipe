import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import './AuthForm.css';

const NewAuthForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    try {
      const response = await axios.post('/auth/register', { email, password });

      if (response.status === 201) {
        // On successful registration, navigate back to the login page
        alert('User successfully created!');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Something went wrong during registration!');
    }
  };

  return (
    <form className='auth-form' onSubmit={handleSubmit}>
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

        <div className='input-group'>
            <label>Confirm Password:</label>
            <input
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
            />
        </div>

        {error && <div className='error'>{error}</div>}

        <div className='center'>
            <button type="submit">Create Account</button>
        </div>
        <div className='link'>
            <Link to="/login">Already have an account? Login</Link> {/* Link to login page */}
        </div>
    </form>
  );
};

export default NewAuthForm;
