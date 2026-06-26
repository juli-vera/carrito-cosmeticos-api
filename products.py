from database import get_connection


class ProductRepository:
    """Repositorio de productos con persistencia en SQLite."""

    def get_all(self):
        conn = get_connection()
        productos = conn.execute("SELECT * FROM products").fetchall()
        conn.close()
        return [dict(p) for p in productos]

    def get_by_id(self, product_id):
        conn = get_connection()
        producto = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)
                                ).fetchone()
        conn.close()
        return dict(producto) if producto else None
