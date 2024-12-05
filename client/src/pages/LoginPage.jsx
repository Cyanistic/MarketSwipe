import './LoginPage.css';
import React, { useState } from 'react';
import AuthForm from '../components/AuthForm';
import { Link } from 'react-router-dom';


const LoginPage = () => {

  return (
    <div className='login-page'>
      <h2>Login</h2>
      <AuthForm />

      <div className="contact-support">
        <Link to="/support" className="contact-support-link">Contact Support</Link>
      </div>
    </div>
  );
};

export default LoginPage;

