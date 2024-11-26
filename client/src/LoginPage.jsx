import React, { useState } from 'react';

const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault(); // Prevents the default form submission
    console.log('Username:', username);
    console.log('Password:', password);
    // Add your authentication logic here
    alert(`Welcome, ${username}!`);
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Account Login</h1>
      <form
        onSubmit={handleSubmit}
        style={{
          display: 'inline-block',
          padding: '80px',
          border: '1px solid #ccc',
          borderRadius: '5px',
          backgroundColor: '#f9f9f9',
          boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
        }}
      >
        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="username" style={{ display: 'block', marginBottom: '5px', marginRight: '113px', fontWeight: 'bold' }}>
            Username
          </label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{
              padding: '10px',
              width: '100%',
              border: '1px solid #ccc',
              borderRadius: '5px',
            }}
            placeholder="Enter your username"
            required
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label htmlFor="password" style={{ display: 'block', marginBottom: '5px', marginRight: '113px', fontWeight: 'bold' }}>
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              padding: '10px',
              width: '100%',
              border: '1px solid #ccc',
              borderRadius: '5px',
            }}
            placeholder="Enter your password"
            required
          />
        </div>

        <button
          type="submit"
          style={{
            padding: '10px 20px',
            marginTop: '30px',
            backgroundColor: '#007BFF',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          Login
        </button>

        <button
          type="submit"
          style={{
            padding: '10px 20px',
            marginTop: '30px',
            marginLeft: '50px',
            backgroundColor: '#8f8f8f',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
          }}
        >
          Return
        </button>
      </form>
      <p style={{ marginTop: '15px' }}>
        Don't have an account? <a href="/signup" style={{ color: '#007BFF', textDecoration: 'none' }}>Sign Up</a>
      </p>
    </div>
  );
};

export default LoginPage;
