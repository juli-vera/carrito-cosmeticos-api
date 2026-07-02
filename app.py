from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from flasgger import Swagger

from database import init_db
from cart import CartManager
from products import ProductRepository

# Crea la aplicacion Flask
app = Flask(__name__)

# Permite conexiones desde el frotend
CORS(app)

# activa swagger
Swagger(app)

# crea base de datos si no existe
init_db()

# Crea objetos que administran productos y carrito
product_repo = ProductRepository()
cart_manager = CartManager()

# Pagina principal


@app.route("/")
def home():
    return render_template("index.html")

# Lista productos


@app.route("/products", methods=["GET"])
def list_products():
    """
    Listar todos los productos
    ---
    responses:
      200:
        description: Lista de productos
    """
    productos = product_repo.get_all()
    return jsonify(productos), 200


@app.route("/cart", methods=["GET"])
def get_cart():
    """
    Ver carrito
    ---
    responses:
      200:
        description: Productos del carrito
    """
    carrito = cart_manager.get_items()
    resultado = []
    for item in carrito:
        producto = product_repo.get_by_id(item["product_id"])
        if producto is not None:
            datos_producto = {
                "product_id": item["product_id"],
                "name": producto["name"],
                "price": producto["price"],
                "quantity": item["quantity"],
            }
            resultado.append(datos_producto)
    return jsonify(resultado), 200


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
      400:
        description: Parámetros inválidos
      404:
        description: Producto no encontrado
    """
    datos = request.get_json()

    # Verificar que exista un JSON
    if datos is None:
        return jsonify({"error": "Se requiere product_id"}), 400

  # Verificar que venga id del producto
    if "product_id" not in datos:
        return jsonify({"error": "Se requiere product_id"}), 400

    # Buscar producto
    producto = product_repo.get_by_id(datos["product_id"])

    if producto is None:
        return jsonify({"error": "Producto no encontrado"}), 404

   # sin no envian cantidad, es 1
    if "quantity" in datos:
        cantidad = datos["quantity"]
    else:
        cantidad = 1

    # Valida cantidad
    if cantidad < 1:
        return jsonify({"error": "La cantidad debe ser un entero positivo"}), 400

    # Agrega al carrito
    cart_manager.add_item(producto["id"], cantidad)

    return jsonify({"message": "Producto agregado al carrito"}), 200


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
        description: Producto no encontrado en el carrito
    """
    eliminado = cart_manager.remove_item(product_id)
    if eliminado:
        return jsonify({"message": "Producto eliminado del carrito"}), 200
    else:
        return jsonify({"error": "Producto no encontrado en el carrito"}), 404


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
    respuesta = {"total": total}
    return jsonify(respuesta), 200


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
