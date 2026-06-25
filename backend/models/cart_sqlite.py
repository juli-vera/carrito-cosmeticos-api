import sqlite3


class CartManager:
    """Gestiona el carrito de compras con persistencia en SQLite."""

    def __init__(self):
        self.db_path = "shop.db"

    def add_item(self, product_id, quantity):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cart (product_id, quantity) VALUES (?, ?)", (product_id, quantity))
        conn.commit()
        conn.close()

    def get_items(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT product_id, quantity FROM cart")
        items = cursor.fetchall()
        conn.close()
        return items

    def get_total(self, product_repo):
        items = self.get_items()
        total = 0
        for item in items:
            product = product_repo.get_by_id(item["product_id"])
            if product:
                total += product["price"] * item["quantity"]
        return total

    def remove_item(self, product_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE product_id = ?", (product_id,))
        conn.commit()
        conn.close()
