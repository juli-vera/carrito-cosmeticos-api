from database import get_connection


class CartManager:
    """Gestiona el carrito de compras"""

    # Devuelve todos los productos del carrito
    def get_items(self):

        conexion = get_connection()

        consulta = conexion.execute("SELECT * FROM cart_items")

        items = consulta.fetchall()

        conexion.close()

        lista_items = []

        for item in items:
            lista_items.append(dict(item))

        return lista_items

    # Agrega un producto al carrito
    def add_item(self, product_id, quantity=1):
        conexion = get_connection()
        consulta = conexion.execute(
            "SELECT * FROM cart_items WHERE product_id = ?", (product_id,))

        producto = consulta.fetchone()

        if producto is None:

            conexion.execute(
                "INSERT INTO cart_items VALUES (?, ?)",
                (product_id, quantity)
            )

        else:
            conexion.execute(
                "UPDATE cart_items SET quantity = quantity + ? WHERE product_id = ?",
                (quantity, product_id)
            )
        conexion.commit()
        conexion.close()

    # Elimina producto del carrito
    def remove_item(self, product_id):
        conexion = get_connection()
        resultado = conexion.execute(
            "DELETE FROM cart_items WHERE product_id = ?", (product_id,)
        )
        conexion.commit()
        conexion.close()
        if resultado.rowcount > 0:
            return True
        else:
            return False

    # vacia el carrito
    def clear(self):
        conexion = get_connection()
        conexion.execute("DELETE FROM cart_items")
        conexion.commit()
        conexion.close()

    # calcula total de la compra
    def calculate_total(self, product_repo):
        total = 0
        items = self.get_items()
        for item in items:
            producto = product_repo.get_by_id(item["product_id"])
            if producto is not None:
                subtotal = producto["price"] * item["quantity"]
                total = total + subtotal
        return total
