import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'hackathon.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS products (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            category      TEXT,
            current_stock INTEGER DEFAULT 0,
            reorder_point INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS vendors (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            name              TEXT    NOT NULL,
            email             TEXT,
            reliability_score REAL    DEFAULT 0,
            lead_time_days    INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS product_vendors (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id    INTEGER NOT NULL,
            vendor_id     INTEGER NOT NULL,
            price         REAL    NOT NULL,
            min_order_qty INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id),
            FOREIGN KEY (vendor_id)  REFERENCES vendors(id)
        );
    ''')

    conn.commit()
    conn.close()
    print("Database initialized.")