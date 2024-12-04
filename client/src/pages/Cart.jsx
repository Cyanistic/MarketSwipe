import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Cart.css";
import { BASE_URL } from "../App";

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);

  useEffect(() => {
    const fetchCart = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/api/cart/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setCartItems(response.data);
      } catch (error) {
        console.error("Error fetching cart items:", error);
      }
    };
    fetchCart();
  }, []);

  return (
    <div className="cart-container">
      <h2 className="cart-title">Your Cart</h2>
      {cartItems.length === 0 ? (
        <p className="cart-empty-message">No items in cart.</p>
      ) : (
        <ul className="cart-item-list">
          {cartItems.map((item) => (
            <li key={item.product_id} className="cart-item">
              <span className="cart-item-id">Product ID: {item.product_id}</span>, 
              Quantity: {item.quantity}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Cart;
