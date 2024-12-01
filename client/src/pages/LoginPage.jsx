import './LoginPage.css';
import React, { useState } from 'react';
import AuthForm from '../components/AuthForm';

const LoginPage = () => {

  return (
    <div className='login-page'>
      <h2>Login</h2>
      <AuthForm />
    </div>
  );
};

export default LoginPage;

