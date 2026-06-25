
class CartManager_1:
    """Gestiona el carrito de compras en memoria."""

    def __init__(self):
        self._items = {}

    def get_items(self):
        items = []
        for pid, qty in self._items.items():
            item = {
                "product_id": pid,
                "quantity": qty
            }
            items.append(item)
        return items

    def add_item(self, product_id, quantity=1):
        if product_id in self._items:
            self._items[product_id] = self._items[product_id] + quantity
        else:
            self._items[product_id] = quantity

    def remove_item(self, product_id):
        if product_id not in self._items:
            return False

        del self._items[product_id]
        return True

    def clear(self):
        self._items.clear()

    def calculate_total(self, product_repo):
        total = 0
        for pid, qty in self._items.items():
            product = product_repo.get_by_id(pid)
            if product:
                total = total + (product["price"] * qty)
        return total
