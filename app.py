from flask import Flask, jsonify, request
from flasgger import Swagger
from cart import CartManager
from products import ProductRepository

app = Flask(__name__)
Swagger(app)

product_repo = ProductRepository()
cart_manager = CartManager()

# PRODUCTOS


@app.route("/products", methods=["GET"])
def list_products():
    """
    Listar todos los productos
    ---
    responses:
        200:
          description: Lista de productos
    """

    products = product_repo.get_all()

    return jsonify(products), 200


# CARRITO

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

    for item in items:
        product = product_repo.get_by_id(item["product_id"])

        if product:
            result.append({
                "product_id": item["product_id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": item["quantity"]
            })

    return jsonify(result), 200


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
    data = request.get_json()
    if not data or "product_id" not in data:
        return jsonify({"error": "Se requiere product_id"}), 400

    product = product_repo.get_by_id(data["product_id"])
    if not product:
        return jsonify({"error: Producto no encontrado"}), 404

    quantity = data.get("quantity", 1)

    if quantity < 1:
        return jsonify({"error": "La cantidad debe ser un entero positivo"}), 400

    cart_manager.add_item(product["id"], quantity)

    return jsonify({
        "message": "Producto agregado al carrito"}), 200


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
    removed = cart_manager.remove_item(product_id)

    if not removed:
        return jsonify({"error": "Producto no encontrado en el carrito"}), 404
    return jsonify({
        "message": "Producto eliminado del carrito"
    }), 200


@app.route("/cart/total", methods=["GET"])
def get_total():
    """
    Calcular total
    ---
    responses:
      200:
        description: Total del carrito
    """
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
