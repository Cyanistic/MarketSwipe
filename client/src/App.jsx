import './App.css';
import React from 'react';
import { useRoutes, Link } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import CreateUser from './pages/CreateUser';
import Shopping from './pages/Shopping';

export const BASE_URL = import.meta.env.DEV ? "http://localhost:5000" : "";

const App = () => {
  // Sets up routes
  let element = useRoutes([
    {
      path: "/shopping",
      element: (
        <div className="fullPage">
          <Shopping />
        </div>
      ),
    },
    {
      path: "/login",
      element: (
        <div className="fullPage">
          <LoginPage />
        </div>
      ),
    },
    {
      path: "/new",
      element: (
        <div className="fullPage">
          <CreateUser />
        </div>
      ),
    },
    {
      path: "/",
      element: (
        <div className="App">
          <div className="header">
            <h1 className='mainHeader'>WELCOME TO <span>MARKET SWIPE</span></h1>
            <h2 className="slogan">Swipe Your Way to Smarter Shopping</h2>
          </div>
          <div className="description">
            <p>
              Market Swipe is the ultimate platform for savvy shoppers. Discover, compare, and shop for the best products with ease. 
              Whether you're looking for daily essentials or unique finds, Market Swipe helps you make informed decisions with a swipe.
            </p>
          </div>
          <Link to="/shopping">
            <button className="centerButton">Start Shopping Now!</button>
          </Link>
        </div>
      ),
    },
  ]);

  return element;
};

export default App;
