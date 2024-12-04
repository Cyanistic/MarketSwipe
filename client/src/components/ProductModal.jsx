import React from "react";
import Modal from "react-modal";
import "./productModal.css";

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
        <h2>{product?.name}</h2>
        <p>{product?.description}</p>
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
