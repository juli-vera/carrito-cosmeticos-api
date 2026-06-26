from database import get_connection


class ProductRepository:
    """Repositorio de productos con persistencia en SQLite."""

    def get_all(self):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT id, name, price FROM products ORDER BY id").fetchall()
        return [dict(r) for r in rows]

    def get_by_id(self, product_id: int):
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id, name, price FROM products WHERE id = ?", (
                    product_id,)
            ).fetchone()
        return dict(row) if row else None
