# This script creates a SQLite database with the following tables:
# user, session, category, product, swipe_history, shopping_cart, orders, order_items, payment, order_history, support_message
import sqlite3

database = 'marketswipe.db'

create_tables = [ 
    """CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        name TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""",
    """CREATE TABLE IF NOT EXISTS session (
        session_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        logout_time TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user (id)
    );""",
    """CREATE TABLE IF NOT EXISTS category (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT
    );""",
    """CREATE TABLE IF NOT EXISTS product (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category_id INTEGER NOT NULL,
        price INTEGER NOT NULL,
        seller TEXT NOT NULL,
        color TEXT,
        size TEXT,
        material TEXT,
        description TEXT,
        image BLOB,
        FOREIGN KEY (category_id) REFERENCES category (id)
    );""",
    """CREATE TABLE IF NOT EXISTS swipe_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        swipe_action TEXT CHECK(swipe_action IN ('like', 'dislike')) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (id),
        FOREIGN KEY (product_id) REFERENCES product (id)
    );""",
    """CREATE TABLE IF NOT EXISTS shopping_cart (
        cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER DEFAULT 1 NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (id),
        FOREIGN KEY (product_id) REFERENCES product (id)
    );""",
    """CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_cost INTEGER NOT NULL,
        status TEXT DEFAULT 'pending',
        FOREIGN KEY (user_id) REFERENCES user (id)
    );""",
    """CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER DEFAULT 1 NOT NULL,
        cost_per_item INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (order_id),
        FOREIGN KEY (product_id) REFERENCES product (id)
    );""",
    """CREATE TABLE IF NOT EXISTS payment (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        amount INTEGER NOT NULL,
        payment_method TEXT NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (order_id)
    );""",
    """CREATE TABLE IF NOT EXISTS order_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        order_id INTEGER NOT NULL,
        purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user (id),
        FOREIGN KEY (order_id) REFERENCES orders (order_id)
    );""",
    """CREATE TABLE IF NOT EXISTS support_message (
        message_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        message_text TEXT NOT NULL,
        message_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        response_text TEXT,
        response_time TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES user (id)
    );"""
]

try:
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()
        for table in create_tables:
            cursor.execute(table)   
        conn.commit()
        print("Tables created successfully.")
        cursor.execute(table)
except sqlite3.OperationalError as e:
    print("Failed to create tables:", e)
