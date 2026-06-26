API REST - Carrito de Compras de Cosméticos
Descripción
Este proyecto consiste en el desarrollo de una API REST utilizando Flask para gestionar un carrito de compras de cosméticos.

La aplicación permite:

Listar productos
Agregar productos al carrito
Ver el contenido del carrito
Eliminar productos del carrito
Calcular el total de la compra
Vaciar el carrito
Tecnologías utilizadas
Python
Flask
Flasgger (Swagger)
unittest
Instalación

1. Clonación del repositorio
   git clone <url-del-repositorio>
2. Entrar a la carpeta del proyecto
   cd cosmeticos
3. Se crea el entorno virtual
   python -m venv .venv
4. Se activa entorno virtual
   Windows
   .venv\Scripts\activate
   Instalación de dependencias
   pip install flask flasgger
   Ejecutación de la aplicación
   python app.py
   La API se ejecutará en:

http://localhost:5000
Documentación Swagger
La documentación interactiva de la API se encuentra en:

http://localhost:5000/apidocs
Desde Swagger se pueden probar los endpoints.

Endpoints principales
Obtener productos
GET /products
Devuelve la lista de productos.

Ver carrito
GET /cart
Devuelve los productos agregados al carrito.

Agregar producto al carrito
POST /cart/items
Ejemplo de comando en consola:

Invoke-RestMethod -Method POST http://localhost:5000/cart/items -ContentType "applicati
on/json" -Body '{"product_id": 1, "quantity": 1}'
Eliminar producto del carrito
DELETE /cart/items/{product_id}
Ejemplo de comando en consola:

Invoke-RestMethod -Method DELETE http://localhost:5000/cart/items/1
Obtener total del carrito
GET /cart/total
Vaciar carrito
DELETE /cart
Tests unitarios con unittest
Para ejecutarlos:

python test_app.py
Para ver que este bien cada metodo:

python -m unittest <archivo>,<clase>,<metodo>
Estructura del proyecto
cosmeticos/
│
├── app.py
├── cart.py
├── products.py
├── test_app.py
├── requirements.txt
└── README.md
