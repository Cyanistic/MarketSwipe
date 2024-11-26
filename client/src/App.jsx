import React from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import './App.css';
import LoginPage from './LoginPage.jsx';

const App = () => {
  const navigate = useNavigate();

  const handleLoginClick = () => {
    console.log('Log in button pressed!');
    navigate('/login'); // Navigate to the login page
  };

  return (
    <div>
      <Routes>
        {/* Define routes */}
        <Route
          path="/"
          element={
            <div style={{ textAlign: 'center', marginTop: '50px' }}>
              <h1>Market Swipe</h1>
              <button
                onClick={handleLoginClick}
                style={{
                  padding: '10px 20px',
                  backgroundColor: '#007BFF',
                  color: 'white',
                  border: 'none',
                  borderRadius: '5px',
                  cursor: 'pointer',
                  marginTop: '20px',
                }}
              >
                Log In 
              </button>
            </div>
          }
        />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
    </div>
  );
};

export default App;
