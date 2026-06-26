from database import get_connection


class CartManager:
    """Gestiona el carrito de compras con persistencia en SQLite."""

    def get_items(self):
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT product_id, quantity FROM cart_items"
            ).fetchall()
        return [dict(r) for r in rows]

    def add_item(self, product_id: int, quantity: int = 1):
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO cart_items (product_id, quantity)
                VALUES (?, ?)
                ON CONFLICT(product_id) DO UPDATE
                    SET quantity = quantity + excluded.quantity
                """,
                (product_id, quantity),
            )

    def remove_item(self, product_id: int) -> bool:
        with get_connection() as conn:
            cur = conn.execute(
                "DELETE FROM cart_items WHERE product_id = ?", (product_id,)
            )
        return cur.rowcount > 0

    def clear(self):
        with get_connection() as conn:
            conn.execute("DELETE FROM cart_items")

    def calculate_total(self, product_repo) -> int:
        total = 0
        for item in self.get_items():
            product = product_repo.get_by_id(item["product_id"])
            if product:
                total += product["price"] * item["quantity"]
        return total
