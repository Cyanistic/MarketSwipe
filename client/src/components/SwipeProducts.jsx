import React, { useState, useEffect } from "react";
import TinderCard from "react-tinder-card";
import axios from "axios";
import { BASE_URL } from '../App';

const SwipeProducts = () => {
  const [products, setProducts] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [loading, setLoading] = useState(true);
  const [likeList, setLikeList] = useState([]);
  const [skipped, setSkipped] = useState([]);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/api/products/`);
        setProducts(response.data);
        setLoading(false);
      } catch (error) {
        console.error("Error fetching products:", error);
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  const handleSwipe = (direction) => {
    const currentProduct = products[currentIndex];
    if (direction === "right") {
      setLikeList([...likeList, currentProduct]);
    } else if (direction === "left") {
      setSkipped([...skipped, currentProduct]);
    }
  
    if (currentIndex < products.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      console.log("No more products!");
    }
  };

  if (loading) {
    return <p>Loading products...</p>;
  }

  if (currentIndex >= products.length) {
    return <p>No more products to show!</p>;
  }

  return (
    <div className="swipe-container">
      <TinderCard
        key={products[currentIndex].id}
        onSwipe={(dir) => handleSwipe(dir)}
        className="swipe-card"
      >
        <div>
          <h3>{products[currentIndex].name}</h3>
          <img
            src={products[currentIndex].image}
            alt={products[currentIndex].name}
            style={{ width: "100%", borderRadius: "10px" }}
          />
          <p>{products[currentIndex].description}</p>
        </div>
      </TinderCard>
    </div>
  );
};

export default SwipeProducts;
