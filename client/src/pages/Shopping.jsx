import './Shopping.css';
import React, { useState } from 'react';

import SwipeProducts from "../components/SwipeProducts";
import ProductModal from "../components/ProductModal";

const Shopping = () => {
  const [products, setProducts] = useState([
    { id: 1, name: "Product A", description: "Description A", image: "linkA" },
    { id: 2, name: "Product B", description: "Description B", image: "linkB" },
  ]);

  return (
    <div>
      <SwipeProducts products={products} />
    </div>
  );
};

export default Shopping;

