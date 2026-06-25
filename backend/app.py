from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger
from models.products_sqlite import ProductRepository
from models.cart_sqlite import CartManager

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

# Inicializar repositorios
product_repo = ProductRepository()
cart_manager = CartManager()

# ------------------- ENDPOINTS -------------------


@app.route("/products", methods=["GET"])
def get_products():
    """
    Obtener todos los productos
    ---
    responses:
      200:
        description: Lista de productos
    """
    products = product_repo.get_all()
    return jsonify(products), 200


@app.route("/cart/items", methods=["POST"])
def add_to_cart():
    """
    Agregar producto al carrito
    ---
    parameters:
      - name: product_id
        in: body
        type: integer
      - name: quantity
        in: body
        type: integer
    responses:
      201:
        description: Producto agregado
    """
    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)
    cart_manager.add_item(product_id, quantity)
    return jsonify({"message": "Producto agregado al carrito"})


@app.route("/cart", methods=["GET"])
def get_cart():
    """
    Ver carrito
    ---
    responses:
      200:
        description: Productos del carrito
    """
    items = cart_manager.get_items()
    result = []
    for product_id, quantity in items:
        product = product_repo.get_by_id(product_id)
        if product:
            result.append({
                "id": product[0],
                "name": product[1],
                "price": product[2],
                "quantity": product[3]
            })
    return jsonify(result)


@app.route("/cart/total", methods=["GET"])
def get_cart_total():
    """
    Total del carrito
    ---
    responses:
      200:
        description: Total calculado
    """
    items = cart_manager.get_items()
    total = 0
    for product_id, quantity in items:
        product = product_repo.get_by_id(product_id)
        if product:
            total += product[2] * quantity
    return jsonify({"total": total})


@app.route("/cart/items/<int:product_id>", methods=["DELETE"])
def delete_from_cart(product_id):
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
        description: Producto eliminado del carrito
    """
    cart_manager.remove_item(product_id)
    return jsonify({"message": f"Producto {product_id} eliminado del carrito"}), 200
