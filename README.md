API REST - Carrito de Compras de Cosméticos

Descripción: En este proyecto se desarrolló una API REST utilizando Flask para gestionar un carrito de compras de cosméticos.

La aplicación lista productos, agrega productos al carrito, permite ver el contenido del carrito, eliminar productos del carrito, calcula el total de la compra y vacia el carrito.

Tecnologías utilizadas: Python, Flask, Flasgger (Swagger), unittest.

Instalación

1. Clonación del repositorio
   git clone <url-del-repositorio>
2. Entrar a la carpeta del proyecto
   cd cosmeticos
3. Se crea el entorno virtual
   python -m venv venv
4. Se activa entorno virtual
   Windows
   venv\Scripts\activate
   Instalación de dependencias
   pip install flask flasgger

   Ejecutación de la aplicación:
   set FLASK_APP=app.py y flask --app app run

La API se ejecutará en: http://localhost:5000

Documentación Swagger de la API se encuentra en: http://localhost:5000/apidocs
Desde Swagger se pueden probar los endpoints.

Endpoints principales

- Obtener productos

GET /products: Devuelve la lista de productos.

- Ver carrito

GET /cart: Devuelve los productos agregados al carrito.

- Agregar producto al carrito

POST /cart/items

Ejemplo de comando en consola:

Invoke-RestMethod -Method POST http://localhost:5000/cart/items -ContentType "applicati
on/json" -Body '{"product_id": 1, "quantity": 1}'

- Eliminar producto del carrito

DELETE /cart/items/{product_id}

Ejemplo de comando en consola:

Invoke-RestMethod -Method DELETE http://localhost:5000/cart/items/1

- Obtener total del carrito

GET /cart/total

- Vaciar carrito

DELETE /cart

Tests unitarios con unittest
Para ejecutarlos:

python test_app.py
Para ver que este bien cada metodo:

python -m unittest <archivo>,<clase>,<metodo>
Estructura del proyecto
cosmeticos/
│
|──templates
| ├──index.html
|──tests
| ├──conftest.py
| ├──test_api.py
| ├──test_e2e.py
|
├── app.py
├── cart.py
├── products.py
├── test_app.py
├── requirements.txt
└── README.md

## Dificultades encontradas y cómo se resolvieron

### 1. Cambio de base de datos: de MySQL a SQLite

**Problema:** Inicialmente se planificó usar MySQL como motor de base de datos,
pero surgieron problemas de acceso y configuración que impedían continuar.  
**Solución:** Se optó por SQLite como alternativa, lo cual simplificó la
configuración al no requerir un servidor externo. Al tener SQLite incluido en
Python, resultó suficiente para utilizarlo en el proyecto.

### 2. Conflictos al subir cambios a GitHub

**Problema:** Al hacer push los cambios no se actualizaban en el
repositorio remoto.
**Solución:** Se resolvieron los conflictos desde VS Code usando la opción
"Aceptar cambio actual" en cada archivo con conflicto, y luego se forzó
la subida con `git push origin main --force`.

### 3. Entorno virtual corrupto

**Problema:** El entorno virtual apuntaba a una ruta incorrecta, lo que
impedía instalar paquetes con pip.  
**Solución:** Se eliminó el entorno virtual y se creó uno nuevo con
`python -m venv venv`, reinstalando todas las dependencias con
`pip install -r requirements.txt`.
