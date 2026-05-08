
class ProductRepository:
    """Repositorio de productos con persistencia en memoria."""

    def __init__(self):
        self._products = {
            1: {"id": 1, "name": "Mascarilla",       "price": 3800},
            2: {"id": 2, "name": "Crema hidratante",    "price": 4810},
            3: {"id": 3, "name": "Contorno de ojos",     "price": 9300},
            4: {"id": 4, "name": "Base",      "price": 10000},
            5: {"id": 5, "name": "Corrector", "price": 8900},
            6: {"id": 6, "name": "Sombra de ojos",      "price": 2600},
            7: {"id": 7, "name": "Delineador",     "price": 1800},
            8: {"id": 8, "name": "Labial",      "price": 5900},
        }

    def get_all(self):
        return list(self._products.values())

    def get_by_id(self, product_id):
        return self._products.get(product_id)
