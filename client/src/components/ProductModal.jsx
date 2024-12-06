import React from "react";
import Modal from "react-modal";
import "./ProductModal.css";

const ProductModal = ({ isOpen, closeModal, product }) => {
  return (
    <Modal
      isOpen={isOpen}
      onRequestClose={closeModal}
      contentLabel="Product Details"
      ariaHideApp={false}
      className="modal-container"
    >
      <div>
        <h1>{product?.name}</h1>
        <h2>Price: ${product?.price}</h2>
        <img
          src={product?.uploads?.[0]?.url || ""}
          alt={product?.name}
        />
      </div>
      <button onClick={closeModal} className="modal-close-button">
        Close
      </button>
    </Modal>
  );
};

export default ProductModal;
