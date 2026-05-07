# Importo Flask para crear la aplicacion, jsonify devuelve respuestas en formato JSON, y request lee datos que envia el cliente.
from flask import Flask, jsonify, request
from flasgger import Swagger
from cart import CartManager  # Importo clase que maneja logica del carrito
# Importo clase que maneja logica de los productos
from products import ProductRepository

"""Creo la aplicacion Flask. __name__ indica a Flask donde buscar archivo"""
app = Flask(__name__)
Swagger(app)

"""Creo instancia del repositorio de productos y otra de carrito para usarlas en endpoints"""
product_repo = ProductRepository()
cart_manager = CartManager()

# PRODUCTOS

# Defino endpoint GET en ruta /products para listar los productos


@app.route("/products", methods=["GET"])
def list_products():  # Defino la función que se ejecuta cuando se llama ese endpoint
    """
    Listar todos los productos
    ---
    responses:
        200:
          description: Lista de productos
    """

    # Obtengo todos los productos desde el repositorio
    products = product_repo.get_all()
    # Devuelvo los productos en formato JSON con código 200, que indica éxito
    return jsonify(products), 200


# CARRITO

# Endpoint para ver el contenido del carrito
@app.route("/cart", methods=["GET"])
# Esta función se ejecuta cuando se consulta ese endpoint
def get_cart():
    """
    Ver carrito
    ---
    responses:
      200:
        description: Productos del carrito
    """

    items = cart_manager.get_items()  # Obtengo los productos que están en el carrito
    result = []  # Creo una lista vacía donde voy a construir la respuesta final

    for item in items:
        product = product_repo.get_by_id(item["product_id"])

        if product:
            result.append({
                "product_id": item["product_id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": item["quantity"]
            })

    return jsonify(result), 200  # Devuelvo productos en formato json


# Endpoint para agregar productos al carrito
@app.route("/cart/items", methods=["POST"])
def add_to_cart():
    """
    Agregar producto al carrito
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          properties:
            product_id:
              type: integer
            quantity:
              type: integer

    responses:
      200:
        description: Producto agregado
      404:
        description: Producto no encontrado
    """
    data = request.get_json()  # Obtengo los datos enviados por el cliente en formato JSON
    if not data or "product_id" not in data:
        return jsonify({"error": "Se requiere product_id"}), 400

    # Busco el producto en el repositorio
    product = product_repo.get_by_id(data["product_id"])
    if not product:  # Si el producto no existe, devuelvo error 404
        return jsonify({"error: Producto no encontrado"}), 404

    # Obtengo la cantidad, y si no viene, uso 1 por defecto
    quantity = data.get("quantity", 1)

    # Valido la cantidad
    if quantity < 1:
        return jsonify({"error": "La cantidad debe ser un entero positivo"}), 400

    # Agrego el producto al carrito con la cantidad indicada
    cart_manager.add_item(product["id"], quantity)
    # Devuelvo mensaje de exito
    return jsonify({
        "message": "Producto agregado al carrito"}), 200

# Endpoint para eliminar un producto del carrito por su ID


@app.route("/cart/items/<int:product_id>", methods=["DELETE"])
def remove_from_cart(product_id):
    """
    Eliminar producto del carrito
    ---
    parameters:
      - name: product_id
        in: path
        type: integer
        required: true

    responses:
      200:
        description: Producto eliminado
      404:
        description: Producto no encontrado
    """
    # Intento eliminar el producto del carrito
    removed = cart_manager.remove_item(product_id)
    # Si no estaba en el carrito, devuelvo error
    if not removed:
        return jsonify({"error": "Producto no encontrado en el carrito"}), 404
    # Si se eliminó correctamente, devuelvo éxito
    return jsonify({
        "message": "Producto eliminado del carrito"
    }), 200

# Endpoint calcula el total del carrito


@app.route("/cart/total", methods=["GET"])
def get_total():
    """
    Calcular total
    ---
    responses:
      200:
        description: Total del carrito
    """
    # Uso los precios del repo para calcular el total
    total = cart_manager.calculate_total(product_repo)
    return jsonify({"Total": total}), 200


@app.route("/cart", methods=["DELETE"])
def clear_cart():
    """
    Vaciar carrito
    ---
    responses:
      200:
        description: Carrito vaciado
    """
    cart_manager.clear()
    return jsonify({"message": "Carrito vaciado exitosamente"}), 200


