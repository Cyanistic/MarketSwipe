import React from "react";

const LikeList = ({ likelist }) => (
  <div>
    <h1>likelist</h1>
    {likelist.length === 0 ? (
      <p>No products in your likes yet!</p>
    ) : (
      likelist.map((product) => (
        <div key={product.id}>
          <h3>{product.name}</h3>
          <img src={product.image} alt={product.name} />
          <p>{product.description}</p>
        </div>
      ))
    )}
  </div>
);

export default LikeList;
