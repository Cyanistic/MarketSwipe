import './Shopping.css';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import SwipeProducts from "../components/SwipeProducts";
import ProductModal from "../components/ProductModal";
import { useLocation } from 'react-router-dom';

const Shopping = () => {
  const { state } = useLocation();
  const { userId, email } = state || {};

  return (
    <div className="shopping-container">
      {/* Link to /cart with an image on the top right */}
      <Link to="/cart" className="cart-link">
        <img
          src="cart-icon.png" // Replace with your image path
          alt="Cart"
          className="cart-image"
        />
        <p  className="cart-text" >Shopping Cart</p> {/* Added text below the image */}
      </Link>

      <SwipeProducts />

      <div className="contact-support">
        <Link to="/support" className="contact-support-link">Contact Support</Link>
      </div>
    </div>
  );
};

export default Shopping;
