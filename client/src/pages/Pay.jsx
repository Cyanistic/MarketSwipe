import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";
import "./Pay.css";
import { BASE_URL } from "../App";

const Pay = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const total = location.state?.total || 0;

  const [formData, setFormData] = useState({
    shippingName: "",
    address: "",
    cardNumber: "",
    expirationDate: "",
    cvv: "",
  });
  const [errors, setErrors] = useState({});

  useEffect(() => {
    if (!location.state?.total) {
      navigate("/cart");
    }
  }, [location.state?.total, navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const validateForm = () => {
    const newErrors = {};
    const { shippingName, address, cardNumber, expirationDate, cvv } = formData;

    if (!shippingName.trim()) newErrors.shippingName = "Shipping name is required.";
    if (!address.trim()) newErrors.address = "Address is required.";
    if (!cardNumber.trim() || cardNumber.length !== 16) {
      newErrors.cardNumber = "Card number must be 16 digits.";
    }
    if (!expirationDate.trim() || !/^\d{2}\/\d{2}$/.test(expirationDate)) {
      newErrors.expirationDate = "Expiration date must be in MM/YY format.";
    }
    if (!cvv.trim() || cvv.length !== 3) {
      newErrors.cvv = "CVV must be 3 digits.";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    try {
      const response = await axios.post(
        `${BASE_URL}/api/orders/create`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      alert(response.data.message);
      navigate("/cart");
    } catch (error) {
      console.error("Error creating order:", error);
      alert(error.response?.data?.message || "Failed to create order");
    }
  };

  const handleCancel = () => {
    navigate("/cart");
  };

  return (
    <div className="pay-container">
      <h2>Checkout</h2>
      <p className="total-amount">Total: ${total.toFixed(2)}</p>
      <form onSubmit={handleSubmit} className="payment-form">
        <div className="form-group">
          <label>Shipping Name</label>
          <input
            type="text"
            name="shippingName"
            value={formData.shippingName}
            onChange={handleInputChange}
          />
          {errors.shippingName && <p className="error-text">{errors.shippingName}</p>}
        </div>
        <div className="form-group">
          <label>Address</label>
          <input
            type="text"
            name="address"
            value={formData.address}
            onChange={handleInputChange}
          />
          {errors.address && <p className="error-text">{errors.address}</p>}
        </div>
        <div className="form-group">
          <label>Card Number</label>
          <input
            type="text"
            name="cardNumber"
            maxLength="16"
            value={formData.cardNumber}
            onChange={handleInputChange}
          />
          {errors.cardNumber && <p className="error-text">{errors.cardNumber}</p>}
        </div>
        <div className="form-group">
          <label>Expiration Date</label>
          <input
            type="text"
            name="expirationDate"
            placeholder="MM/YY"
            value={formData.expirationDate}
            onChange={handleInputChange}
          />
          {errors.expirationDate && (
            <p className="error-text">{errors.expirationDate}</p>
          )}
        </div>
        <div className="form-group">
          <label>CVV</label>
          <input
            type="text"
            name="cvv"
            maxLength="3"
            value={formData.cvv}
            onChange={handleInputChange}
          />
          {errors.cvv && <p className="error-text">{errors.cvv}</p>}
        </div>
        <div className="button-container">
          <button type="submit" className="confirm-button">
            Confirm Transaction
          </button>
          <button type="button" onClick={handleCancel} className="cancel-button">
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default Pay;
