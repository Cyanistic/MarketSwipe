import React, { useState } from 'react';
import axios from 'axios';
import { BASE_URL } from '../App';

const LikeList = () => {
  const [productData, setProductData] = useState({
    name: '',
    price: '',
    category: '',
    tags: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProductData({ ...productData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    const productPayload = {
      name: productData.name,
      price: parseFloat(productData.price),
      category: productData.category,
      tags: productData.tags.split(',').map((tag) => tag.trim()),
    };
  
    // Validate payload
    if (!productPayload.name || !productPayload.price || !productPayload.category) {
      console.error('Invalid payload:', productPayload);
      alert('Please fill in all required fields.');
      return;
    }
  
    try {
      const token = localStorage.getItem('token');
      if (!token) {
        console.error('No token found');
        alert('You must log in to perform this action.');
        return;
      }
  
      console.log('Token:', token);
      console.log('Product Payload:', productPayload);
  
      const response = await axios.post(
        `${BASE_URL}/api/products/`,
        productPayload,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );
  
      console.log('Product created successfully:', response.data);
    } catch (error) {
      console.error('Error creating product:', error.response?.data || error.message);
    }
  };
  

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Product Name:</label>
        <input
          type="text"
          name="name"
          value={productData.name}
          onChange={handleChange}
          placeholder="Product Name"
          required
        />
      </div>
      <div>
        <label>Price:</label>
        <input
          type="number"
          step="0.01"
          name="price"
          value={productData.price}
          onChange={handleChange}
          placeholder="Price"
          required
        />
      </div>
      <div>
        <label>Category:</label>
        <input
          type="text"
          name="category"
          value={productData.category}
          onChange={handleChange}
          placeholder="Category"
          required
        />
      </div>
      <div>
        <label>Tags (comma separated):</label>
        <input
          type="text"
          name="tags"
          value={productData.tags}
          onChange={handleChange}
          placeholder="Tags"
        />
      </div>
      <button type="submit">Create Product</button>
    </form>
  );
};

export default LikeList;
