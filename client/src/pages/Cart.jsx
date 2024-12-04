import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Cart.css";
import { BASE_URL } from "../App";

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);

  // Fetch cart items on component mount
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

  // Remove product from cart
  const removeProductFromCart = async (productId) => {
    try {
      const response = await axios.post(
        `${BASE_URL}/api/cart/remove`,
        { productId },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      alert(response.data.message); // Show success message
      // Re-fetch cart items after removing the product
      setCartItems(cartItems.filter((item) => item.product_id !== productId));
    } catch (error) {
      console.error("Error removing product from cart:", error);
      alert(error.response?.data?.message || "Failed to remove product");
    }
  };

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
              {/* Add Remove button next to each product */}
              <button
                onClick={() => removeProductFromCart(item.product_id)}
                className="remove-product-button"
              >
                Remove
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Cart;
