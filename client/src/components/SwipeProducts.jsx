import React, { useState } from "react";
import TinderCard from "react-tinder-card";
import Modal from "react-modal";

const SwipeProducts = () => {
  const [products] = useState([
    { id: 1, name: "Product A", description: "Description A", image: "linkA" },
    { id: 2, name: "Product B", description: "Description B", image: "linkB" },
    { id: 3, name: "Product C", description: "Description C", image: "linkC" },
  ]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Handle swipe and move to the next product
  const handleSwipe = (direction) => {
    if (currentIndex < products.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      console.log("No more products!");
    }
  };

  // Open modal for more details
  const handleMoreDetails = () => {
    setIsModalOpen(true);
  };

  // Close modal
  const closeModal = () => {
    setIsModalOpen(false);
  };

  // Check for no more products
  if (currentIndex >= products.length) {
    return <p style={{ textAlign: "center" }}>No more products to show!</p>;
  }

  return (
    <div className="swipe-container">
      {/* Swipeable Product */}
      <TinderCard
        key={products[currentIndex].id}
        onSwipe={handleSwipe}
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

      {/* More Details Button */}
      <button
        style={{ marginTop: "20px" }}
        onClick={handleMoreDetails}
      >
        More Details
      </button>

      {/* Modal for Product Details */}
      <Modal
  isOpen={isModalOpen}
  onRequestClose={closeModal}
  contentLabel="Product Details"
  ariaHideApp={false} // Prevent accessibility warnings
  style={{
    content: {
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between', // Ensures content stays spaced
      alignItems: 'center',
      padding: '20px',
      width: '400px',
      height: '300px',
      margin: 'auto',
      borderRadius: '10px',
      textAlign: 'center',
    },
  }}
>
  <div>
    <h2>{products[currentIndex].name}</h2>
    <p>{products[currentIndex].description}</p>
    <img
      src={products[currentIndex].image}
      alt={products[currentIndex].name}
      style={{ width: '100%', borderRadius: '10px' }}
    />
  </div>

  {/* Close button at the bottom */}
  <button
    onClick={closeModal}
    style={{
      marginTop: 'auto', // Ensures it sticks to the bottom
      padding: '10px 20px',
      backgroundColor: '#007bff',
      color: 'white',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
    }}
  >
    Close
  </button>
</Modal>

    </div>
  );
};

export default SwipeProducts;
