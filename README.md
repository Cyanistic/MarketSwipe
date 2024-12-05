<div align="center">
    <img src="./client/public/MarketSwipeLogorp.png" alt="MarketSwipe Logo" width="500">
</div>

MarketSwipe is an intuitive and dynamic e-commerce platform that simplifies product browsing and purchasing through swipe-based interactions. This monorepo contains both the **frontend** (React) and **backend** (Flask) codebases.

---

## Features

- **Swipe Products**: Swipe right to add to cart, swipe left to skip.
- **User Authentication**: Register, log in, and manage user accounts.
- **Product Management**: Upload, browse, and edit products.
- **Cart & Order Management**: Seamlessly add products to the cart, place orders, and view order history.
- **Image Uploads**: Securely upload and access product images.
- **Responsive Design**: Optimized for mobile and desktop devices.

---

## Tech Stack

### Frontend:
- **React**: For building the user interface.
- **Axios**: For API requests.
- **Vite**: Development environment.

### Backend:
- **Flask**: REST API for the application logic.
- **Flask-CORS**: To handle cross-origin requests.
- **SQLAlchemy**: Database ORM.
- **SQLite**: Database for storing data.
- **JWT**: For secure user authentication.

---

## Monorepo Structure

```plaintext
MarketSwipe/
├── client/                # Frontend code
│   ├── src/               # React components, styles, and pages
│   ├── public/            # Static files
│   ├── package.json       # Frontend dependencies
│   └── vite.config.js     # Vite configuration
├── server/                # Backend code
│   ├── migrations/        # Database migrations
│   ├── models/            # Database models
│   ├── routes/            # API endpoints
│   ├── app.py             # Main Flask application
│   ├── requirements.txt   # Backend dependencies
│   └── .env.example       # Example environment variables
└── README.md              # Project documentation
