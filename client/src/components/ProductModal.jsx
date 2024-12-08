import React from "react";
import Modal from "react-modal";
import "./ProductModal.css";
import { BASE_URL } from "../App";


const ProductModal = ({ isOpen, closeModal, product, images}) => {
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
      </div>
      <br></br>
      <button onClick={closeModal} className="modal-close-button">
        Close
      </button>
    </Modal>
  );
};

export default ProductModal;
