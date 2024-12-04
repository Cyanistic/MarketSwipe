import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BASE_URL } from '../App';

const LikeList = () => {
  const [productData, setProductData] = useState({
    name: '',
    price: '',
    category: '',
    tags: '',
  });
  const [categories, setCategories] = useState([]); // List of categories from the backend
  const [customCategory, setCustomCategory] = useState({
    name: '',
    description: '',
  }); // For creating a new category

  // Fetch categories from the backend on component mount
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get(`${BASE_URL}/api/products/categories`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });
        setCategories(response.data); // Assuming the server responds with a list of categories
      } catch (error) {
        console.error('Error fetching categories:', error.response?.data || error.message);
      }
    };

    fetchCategories();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setProductData({ ...productData, [name]: value });
  };

  // Handle category selection
  const handleCategoryChange = (e) => {
    setProductData({ ...productData, category: e.target.value });
  };

  // Handle input for custom category (name and description)
  const handleCustomCategoryChange = (e) => {
    const { name, value } = e.target;
    setCustomCategory({ ...customCategory, [name]: value });
  };

  // Handle adding a new category
  const handleCreateCategory = async () => {
    if (!customCategory.name.trim()) {
      alert('Category name cannot be empty.');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${BASE_URL}/api/products/categories`,
        {
          name: customCategory.name,
          description: customCategory.description, // Include description in the payload
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      const newCategory = response.data.category; // Assuming backend returns the created category
      setCategories([...categories, newCategory]); // Add the new category to the dropdown
      setProductData({ ...productData, category: newCategory.id }); // Set the newly created category
      setCustomCategory({ name: '', description: '' }); // Clear the custom category input
    } catch (error) {
      console.error('Error creating category:', error.response?.data || error.message);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const productPayload = {
      name: productData.name,
      price: parseFloat(productData.price),
      categoryId: productData.category, // Ensure category is the ID
      tags: productData.tags.split(',').map((tag) => tag.trim()),
    };

    const token = localStorage.getItem('token');

    try {
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
        <select
          name="category"
          value={productData.category}
          onChange={handleCategoryChange}
          required
        >
          <option value="" disabled>
            Select a category
          </option>
          {categories.map((category) => (
            <option key={category.id} value={category.id}>
              {category.name}
            </option>
          ))}
        </select>
        <div>
          <label>Add Custom Category:</label>
          <input
            type="text"
            name="name"
            value={customCategory.name}
            onChange={handleCustomCategoryChange}
            placeholder="Custom Category Name"
          />
          <input
            type="text"
            name="description"
            value={customCategory.description}
            onChange={handleCustomCategoryChange}
            placeholder="Custom Category Description"
          />
          <button type="button" onClick={handleCreateCategory}>
            Add Category
          </button>
        </div>
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
