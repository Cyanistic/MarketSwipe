import React from "react";

const HistoryPage = ({ skipped }) => (
  <div>
    <h1>Skipped Products</h1>
    {skipped.length === 0 ? (
      <p>No skipped products yet!</p>
    ) : (
      skipped.map((product) => (
        <div key={product.id}>
          <h3>{product.name}</h3>
          <img src={product.image} alt={product.name} />
          <p>{product.description}</p>
        </div>
      ))
    )}
  </div>
);

export default HistoryPage;
