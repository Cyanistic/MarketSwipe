import React, { useState, useEffect } from "react";
import axios from "axios";
import "./Cart.css";
import { BASE_URL } from "../App";

const Cart = () => {
  const [cartItems, setCartItems] = useState([]);
  const [productDetails, setProductDetails] = useState({});

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
        // Fetch product details for each product in the cart
        fetchProductDetails(response.data);
      } catch (error) {
        console.error("Error fetching cart items:", error);
      }
    };

    const fetchProductDetails = async (cartItems) => {
      const details = {};
      for (const item of cartItems) {
        try {
          const response = await axios.get(`${BASE_URL}/api/products/${item.product}`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          });
          details[item.product] = response.data; // Store product details
        } catch (error) {
          console.error(`Error fetching details for product ${item.product}:`, error);
        }
      }
      setProductDetails(details); // Update the product details in the state
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
      setCartItems(cartItems.filter((item) => item.product !== productId));
    } catch (error) {
      console.error("Error removing product from cart:", error);
      alert(error.response?.data?.message || "Failed to remove product");
    }
  };

  const getTotalPrice = () => {
    return cartItems.reduce((total, item) => {
      const product = productDetails[item.product];
      if (product) {
        return total + product.price * item.quantity;
      }
      return total;
    }, 0);
  };

  return (
    <div className="cart-container">
      <h2 className="cart-title">Your Cart</h2>
      {cartItems.length === 0 ? (
        <p className="cart-empty-message">No items in cart.</p>
      ) : (
        <ul className="cart-item-list">
          {cartItems.map((item) => {
            const product = productDetails[item.product];
            if (!product) return null; // Skip if product details are not loaded yet

            return (
              <li key={item.product} className="cart-item">
                <span className="cart-item-name">{product.name}</span>
                <span className="cart-item-price">${product.price}</span>
                <span className="cart-item-quantity">Quantity: {item.quantity}</span>
                {/* Add Remove button next to each product */}
                <button
                  onClick={() => removeProductFromCart(item.product)}
                  className="remove-product-button"
                >
                  Remove
                </button>
              </li>
            );
          })}
        </ul>
      )}
      <div className="cart-total">
        <strong>Total: ${getTotalPrice().toFixed(2)}</strong>
      </div>
    </div>
  );
};

export default Cart;
