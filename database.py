import sqlite3

DB_PATH = "shop.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id      INTEGER PRIMARY KEY,
            name    TEXT    NOT NULL,
            price   INTEGER NOT NULL
            )
        """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            product_id INTEGER PRIMARY KEY,
            quantity   INTEGER NOT NULL DEFAULT 1
        )
    """)
    conn.commit()

    cantidad = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
    if cantidad == 0:
        productos = [
            (1, "Mascarilla",       3800),
            (2, "Crema hidratante", 4810),
            (3, "Contorno de ojos", 9300),
            (4, "Base",            10000),
            (5, "Corrector",        8900),
            (6, "Sombra de ojos",   2600),
            (7, "Delineador",       1800),
            (8, "Labial",           5900),
        ]
        conn.executemany("INSERT INTO products VALUES (?, ?, ?)", productos)
        conn.commit()

    conn.close()
