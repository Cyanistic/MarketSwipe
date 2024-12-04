import React, { useState, useEffect } from "react";
import TinderCard from "react-tinder-card";
import axios from "axios";
import ProductModal from "./ProductModal";
import { Link } from "react-router-dom";
import "./SwipeProducts.css";
import { BASE_URL } from "../App";

const SwipeProducts = () => {
  const [products, setProducts] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [likedTags, setLikedTags] = useState([]);
  const [swipeDirection, setSwipeDirection] = useState("");

  // Fetch products from the backend
  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/api/products`);
        setProducts(response.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };
    fetchProducts();
  }, []);

  // Filter products based on liked tags
  const filterProductsByTags = () => {
    if (likedTags.length === 0) return products;
    return products.filter((product) =>
      product.tags.some((tag) => likedTags.includes(tag))
    );
  };

  // Update current index and handle liking a product
  const updateIndex = (direction) => {
    const likedProduct = products[currentIndex];
    if (direction === "right") {
      setLikedTags((prevTags) => [
        ...new Set([...prevTags, ...likedProduct.tags]),
      ]);
    }

    // Increment currentIndex
    setCurrentIndex((prevIndex) => {
      if (prevIndex < products.length - 1) {
        return prevIndex + 1;
      } else {
        console.log("No more products!");
        return prevIndex; // No more products to show
      }
    });
  };

  const handleSwipe = (direction) => {
    setSwipeDirection(direction);
    updateIndex(direction);
  };

  const swipeManually = (direction) => {
    setSwipeDirection(direction);
    updateIndex(direction);
  };

  // Modal controls
  const handleMoreDetails = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  const filteredProducts = filterProductsByTags();

  if (currentIndex >= filteredProducts.length) {
    return <p className="swipe-container">No more products to show!</p>;
  }

  return (
    <div className="swipe-products">
      <div className="swipe-container">
        <TinderCard
          key={filteredProducts[currentIndex]?.id}
          onSwipe={handleSwipe}
          className="swipe-card"
          preventSwipe={["up", "down"]}
        >
          <div>
            <h3>{filteredProducts[currentIndex]?.name}</h3>
            <img
              src={filteredProducts[currentIndex]?.uploads?.[0]?.url || ""}
              alt={filteredProducts[currentIndex]?.name}
            />
            <p>{filteredProducts[currentIndex]?.description}</p>
          </div>
        </TinderCard>

        <div className="swipe-buttons">
          <button onClick={() => swipeManually("left")}>Swipe Left</button>
          <button onClick={() => swipeManually("right")}>Swipe Right</button>
        </div>

        <button onClick={handleMoreDetails} className="modal-close-button">
          More Details
        </button>

        <div className="center-buttons">
          <Link to="/likes">
            <button className="centerButton">LikeList</button>
          </Link>

          <Link to="/history">
            <button className="centerButton">History</button>
          </Link>
        </div>

        <ProductModal
          isOpen={isModalOpen}
          closeModal={closeModal}
          product={filteredProducts[currentIndex]}
        />
      </div>
    </div>
  );
};

export default SwipeProducts;
