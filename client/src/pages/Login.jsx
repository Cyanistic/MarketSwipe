import './Login.css';
import React, { useState } from 'react';
import AuthForm from '../components/AuthForm';

const Login = () => {

  return (
    <div className='login-page'>
      <h2>Login</h2>
      <AuthForm />
    </div>
  );
};

export default Login;

