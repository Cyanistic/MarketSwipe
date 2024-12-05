import './Support.css';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';

const Support = () => {
  const [message, setMessage] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (message.trim() === '') {
        alert('Please enter a message before submitting.');
        return;
      }

    console.log('Message submitted:', message);
    setSubmitted(true);
  };

  return (
    <div className="support-container">
      <div className="title-box">
        <h2>Contact Support</h2>
      </div>
      {submitted ? (
        <div className="confirmation">
          <p>Thank you for reaching out! We will get back to you shortly.</p>
          <Link to="/" className="home-button">Go to Home</Link>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="support-form">
          <div className="input-container">
            <label htmlFor="support-message">Describe your issue:</label>
            <textarea
              id="support-message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              rows="5"
              placeholder="Enter your message here..."
            ></textarea>
          </div>
          <div className="button-container">
            <button type="submit" className="submit-button">Submit</button>
            <Link to="/" className="home-button">Go to Home</Link>
          </div>
        </form>
      )}
    </div>
  );
};

export default Support;
