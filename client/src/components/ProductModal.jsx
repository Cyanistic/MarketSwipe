import React, { useState } from "react";
import Modal from "react-modal";
import './ProductModal.css';

const ProductModal = ({ product }) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div>
      <button onClick={() => setIsOpen(true)}>View Details</button>
      <Modal isOpen={isOpen} onRequestClose={() => setIsOpen(false)}>
        <h2>{product.name}</h2>
        <p>{product.description}</p>
        <img src={product.image} alt={product.name} />
        <button onClick={() => setIsOpen(false)}>Close</button>
      </Modal>
    </div>
  );
};

export default ProductModal;
