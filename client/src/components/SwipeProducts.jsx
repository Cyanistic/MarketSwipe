import React, { useState, useEffect } from "react";
import TinderCard from "react-tinder-card";
import axios from "axios";
import ProductModal from "./ProductModal";
import { Link } from "react-router-dom";
import "./SwipeProducts.css";
import { BASE_URL } from "../App";

const SwipeProducts = () => {
  const [currentProduct, setCurrentProduct] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Fetch the initial product
  useEffect(() => {
    const fetchFirstProduct = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/api/products`);
        setCurrentProduct(response.data[0]);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };
    fetchFirstProduct();
  }, []);

  const handleSwipe = (direction) => {
    if (currentProduct) {
      axios
        .post(
          `${BASE_URL}/api/products/swipe`,
          {
            product_id: currentProduct.id,
            liked: direction === "right",
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        )
        .then((response) => {
          const recommendedProduct = response.data;
          setCurrentProduct(recommendedProduct);
        })
        .catch((error) => {
          console.error("Error recording swipe:", error);
        });
    }
  };

  const swipeManually = (direction) => {
    handleSwipe(direction);
  };

  const handleAddToCart = async () => {
    if (!currentProduct) return;

    try {
      const response = await axios.post(
        `${BASE_URL}/api/cart/add`,
        { productId: currentProduct.id },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      alert(response.data.message);
    } catch (error) {
      console.error("Error adding product to cart:", error);
      alert(error.response?.data?.message || "Failed to add product to cart");
    }
  };

  const handleMoreDetails = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  if (!currentProduct) {
    return <p className="swipe-container">Loading products...</p>;
  }

  return (
    <div className="swipe-products">
      <div className="swipe-container">
        <TinderCard
          key={currentProduct?.id}
          onSwipe={handleSwipe}
          className="swipe-card"
          preventSwipe={["up", "down"]}
        >
          <div>
            <h3>{currentProduct?.name}</h3>
            <img
              src={currentProduct?.uploads?.[0]?.url || ""}
              alt={currentProduct?.name}
            />
            <p>{currentProduct?.description}</p>
          </div>
        </TinderCard>

        <div className="swipe-buttons">
          <button onClick={() => swipeManually("left")}>Swipe Left</button>
          <button onClick={() => swipeManually("right")}>Swipe Right</button>
          <button onClick={handleAddToCart} className="add-to-cart-button">
            Add to Cart
          </button>
        </div>

        <button onClick={handleMoreDetails} className="modal-close-button">
          More Details
        </button>

        <div className="center-buttons">
          <Link to="/add-product">
            <button className="centerButton">Create Product</button>
          </Link>

          <Link to="/history">
            <button className="centerButton">History</button>
          </Link>
        </div>

        <ProductModal
          isOpen={isModalOpen}
          closeModal={closeModal}
          product={currentProduct}
        />
      </div>
    </div>
  );
};

export default SwipeProducts;
