from database import get_connection


class CartManager:
    """Gestiona el carrito de compras con persistencia en SQLite."""

    def get_items(self):
        conn = get_connection()
        items = conn.execute("SELECT * FROM cart_items"
                             ).fetchall()
        conn.close()
        return [dict(i) for i in items]

    def add_item(self, product_id, quantity=1):
        conn = get_connection()
        existe = conn.execute("SELECT * FROM cart_items WHERE product_id = ?", (product_id,)
                              ).fetchone()

        if existe:
            conn.execute(
                "UPDATE cart_items SET quantity = quantity + ? WHERE product_id = ?",
                (quantity, product_id)
            )
        else:
            conn.execute(
                "INSERT INTO cart_items VALUES (?, ?)",
                (product_id, quantity)
            )
        conn.commit()
        conn.close()

    def remove_item(self, product_id):
        conn = get_connection()
        resultado = conn.execute(
            "DELETE FROM cart_items WHERE product_id = ?", (product_id,)
        )
        conn.commit()
        conn.close()
        return resultado.rowcount > 0

    def clear(self):
        conn = get_connection()
        conn.execute("DELETE FROM cart_items")
        conn.commit()
        conn.close()

    def calculate_total(self, product_repo):
        total = 0
        for item in self.get_items():
            producto = product_repo.get_by_id(item["product_id"])
            if producto:
                total += producto["price"] * item["quantity"]
        return total
