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
  const [quantityModalOpen, setQuantityModalOpen] = useState(false);
  const [quantity, setQuantity] = useState(1);
  const [images, setImages] = useState([]);

  // Fetch the initial product
  useEffect(() => {
    const fetchFirstProduct = async () => {
      try {
        const response = await axios.get(`${BASE_URL}/api/products`);
        setCurrentProduct(response.data[0]); // Set the first product
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };
    fetchFirstProduct();
  }, []);

  // Fetch images for the current product
  const fetchProductImages = async (imageIds) => {
    console.log(imageIds)
    setImages(imageIds);
  };

  const handleSwipe = (direction) => {
    if (currentProduct) {
      // Record the swipe
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
          const nextProduct = response.data; // Get the next product from the response

          if (!nextProduct) {
            // If no more products are returned, reset swipe history
            resetSwipeHistory();
          } else {
            // Set the next product as the current product
            setCurrentProduct(nextProduct);
            console.log(nextProduct)
            if (nextProduct?.uploads?.length) {
              fetchProductImages(nextProduct.uploads);
            } else {
              setImages([]); // Clear images if no image IDs
            }
          }
        })
        .catch((error) => {
          if (error.response && error.response.status === 500) {
            // If error 500 occurs, reset the swipe history
            console.log("No more products, resetting swipe history...");
            resetSwipeHistory();
          } else {
            console.error("Error recording swipe:", error);
          }
        });
    }
  };

  const resetSwipeHistory = async () => {
    try {
      await axios.post(
        `${BASE_URL}/api/products/reset`,
        {},
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      alert("All swipe history has been reset!");
      // After resetting, try to fetch the first product again
      const response = await axios.get(`${BASE_URL}/api/products`);
      setCurrentProduct(response.data[0]); // Reset the product list by fetching the first product
    } catch (error) {
      console.error("Error resetting swipe history:", error);
      alert("Failed to reset swipe history.");
    }
  };

  const swipeManually = (direction) => {
    handleSwipe(direction);
  };

  const openQuantityModal = () => {
    setQuantityModalOpen(true);
  };

  const closeQuantityModal = () => {
    setQuantityModalOpen(false);
  };

  const handleQuantityChange = (e) => {
    console.log(e.target.value);
    setQuantity(e.target.value);
  };

  const handleAddToCart = async () => {
    if (!currentProduct || quantity < 1) return;

    const parsedQuantity = parseInt(quantity, 10);

    try {
      console.log(currentProduct.id, parsedQuantity)
      const response = await axios.post(
        `${BASE_URL}/api/cart/add`,
        { productId: currentProduct.id, quantity: parsedQuantity },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );
      alert(response.data.message);
      closeQuantityModal();
    } catch (error) {
      console.error("Error adding product to cart:", error);
      alert(error.response?.data?.message || "Failed to add product to cart");
    }
  };

  const handleMoreDetails = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);

  return (
    <div className="swipe-products">
      <div className="swipe-container">
        {currentProduct ? (
          <>
          <TinderCard
            key={currentProduct?.id}
            onSwipe={handleSwipe}
            className="swipe-card"
            preventSwipe={["up", "down"]}
          >
            <div>
              <h3>{currentProduct?.name}</h3>

              <div className="product-images">
                {images.length > 0 ? (
                  images.map((image, index) => (
                    <img
                      key={index}
                      src={`${BASE_URL}/api/upload/${image.path}`}
                      alt={`Product Image ${index + 1}`}
                      className="product-image"
                    />
                  ))
                ) : (
                  <p>No images available</p>
                )}
              </div>

              <p>{currentProduct?.description}</p>
            </div>
          </TinderCard>

          <div className="swipe-buttons">
            <button onClick={handleMoreDetails} className="more-details-button">
              More Details
            </button>
            <button onClick={() => swipeManually("left")}>Swipe Left</button>
            <button onClick={() => swipeManually("right")}>Swipe Right</button>
            <button onClick={openQuantityModal} className="add-to-cart-button">
              Add to Cart
            </button>
          </div>


          {/* Popup Modal for Quantity Input */}
          {quantityModalOpen && (
            <div className="quantity-modal-overlay">
              <div className="quantity-modal">
                <h3>Select Quantity</h3>
                <input
                  type="number"
                  value={quantity}
                  onChange={handleQuantityChange}
                  min="1"
                  className="quantity-input"
                />

                <div className="quantity-modal-buttons">
                  <button onClick={handleAddToCart} className="confirm-add-to-cart">
                    Add to Cart
                  </button>
                  <button onClick={closeQuantityModal} className="cancel-modal">
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          )}
          </>
        ) : (<p>Loading products...</p>)}

        <div className="center-buttons">
          <Link to="/add-product">
            <button className="centerButton">Create Product</button>
          </Link>

          <Link to="/history">
            <button className="centerButton">Order History</button>
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
