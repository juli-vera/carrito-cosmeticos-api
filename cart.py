
class CartManager:
    """Gestiona el carrito de compras en memoria."""

    def __init__(self):
        self._items = {}  # Uso un diccionario para guardar los productos del carrito, donde la clave es el ID y el valor la cantidad {product_id: quantity}

    # Recorro el diccionario y construyo una lista de objetos con product_id y quantity para devolverlos en formato JSON
    def get_items(self):
        items = []
        for pid, qty in self._items.items():
            item = {
                "product_id": pid,
                "quantity": qty
            }
            items.append(item)
        return items
    # Si el producto ya existe en el carrito, sumo la cantidad. Si no, lo agrego.

    def add_item(self, product_id, quantity=1):
        if product_id in self._items:
            self._items[product_id] = self._items[product_id] + quantity
        else:
            self._items[product_id] = quantity

    # Verifico si el producto está en el carrito. Si está, lo elimino usando del. Si no, retorno False
    def remove_item(self, product_id):
        if product_id not in self._items:
            return False

        del self._items[product_id]
        return True

    # Vacío completamente el carrito
    def clear(self):
        self._items.clear()

    # Recorro los productos del carrito, busco su precio y calculo el total multiplicando precio por cantidad.
    def calculate_total(self, product_repo):
        total = 0
        for pid, qty in self._items.items():
            product = product_repo.get_by_id(pid)
            if product:
                total = total + (product["price"] * qty)
        return total
