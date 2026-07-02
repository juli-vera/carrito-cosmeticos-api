from database import get_connection


class ProductRepository:
    """Repositorio de productos"""

    # Devuelve todos los productos
    def get_all(self):
        conexion = get_connection()
        productos = conexion.execute("SELECT * FROM products").fetchall()
        conexion.close()
        lista_productos = []
        for producto in productos:
            lista_productos.append(dict(producto))
        return lista_productos

    # Busca producto por su id
    def get_by_id(self, product_id):
        conexion = get_connection()
        consulta = conexion.execute(
            "SELECT * FROM products WHERE id = ?", (product_id,))

        producto = consulta.fetchone()
        conexion.close()
        if producto is not None:
            return dict(producto)
        else:
            return None
