import sqlite3
import os

DB_PATH = os.environ.get("DB_PATH", "shop.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS products (
                id      INTEGER PRIMARY KEY,
                name    TEXT    NOT NULL,
                price   INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS cart_items (
                product_id INTEGER PRIMARY KEY,
                quantity   INTEGER NOT NULL DEFAULT 1
            );
        """)

        # Seed products only when the table is empty
        existing = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if existing == 0:
            conn.executemany(
                "INSERT INTO products (id, name, price) VALUES (?, ?, ?)",
                [
                    (1, "Mascarilla",       3800),
                    (2, "Crema hidratante", 4810),
                    (3, "Contorno de ojos", 9300),
                    (4, "Base",            10000),
                    (5, "Corrector",        8900),
                    (6, "Sombra de ojos",   2600),
                    (7, "Delineador",       1800),
                    (8, "Labial",           5900),
                ],
            )
