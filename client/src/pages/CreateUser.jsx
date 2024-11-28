import './CreateUser.css';
import React, { useState } from 'react';
import NewAuthForm from '../components/NewAuthForm';

const CreateUser = () => {

  return (
    <div className='login-page'>
      <h2>Create Account</h2>
      <NewAuthForm />
    </div>
  );
};

export default CreateUser;

