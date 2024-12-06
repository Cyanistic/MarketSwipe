import React, { useEffect, useState } from "react";
import axios from "axios";
import { BASE_URL } from "../App";
import "./HistoryPage.css";
import { Link } from "react-router-dom";

const HistoryPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/api/orders/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        });
        setOrders(response.data); 
      } catch (error) {
        console.error("Error fetching order history:", error);
        setError(error.response?.data?.message || "Failed to fetch orders");
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, []);

  if (loading) return <p>Loading your order history...</p>;

  if (error) return <p className="error">{error}</p>;

  if (orders.length === 0)
    return <p className="empty-message">You have no order history.</p>;

  return (
    <div className="history-container">
      <Link to="/shopping" className="back-link">
        <img src="back.png" alt="Back arrow" className="back-image" />
      </Link>
      <h2>Your Order History</h2>
      <ul className="order-list">
        {orders.map((order) => (
          <li key={order.id} className="order-item">
            <div className="order-header">
              <span className="order-id">Order ID: {order.id}</span>
              <span className="order-date">
                Date: {new Date(order.createdAt).toLocaleDateString()}
              </span>
              <span className="order-status">Status: {order.status}</span>
            </div>
            <ul className="order-products">
              {order.items.map((item, index) => (
                <li key={index} className="product-item">
                  <span className="product-name">
                    {item.product?.name || "Unknown Product"}
                  </span>
                  <span className="product-quantity">
                    Qty: {item.quantity}
                  </span>
                  <span className="product-price">
                    ${item.product?.price?.toFixed(2) || "0.00"}
                  </span>
                </li>
              ))}
            </ul>
            <div className="order-total">
              Total: ${parseFloat(order.total).toFixed(2)}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HistoryPage;
