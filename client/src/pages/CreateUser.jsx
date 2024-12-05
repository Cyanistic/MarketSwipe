import './CreateUser.css';
import React, { useState } from 'react';
import NewAuthForm from '../components/NewAuthForm';
import { Link } from 'react-router-dom';


const CreateUser = () => {

  return (
    <div className='login-page'>
      <h2>Create Account</h2>
      <NewAuthForm />

      <div className="contact-support">
        <Link to="/support" className="contact-support-link">Contact Support</Link>
      </div>
    </div>
  );
};

export default CreateUser;

