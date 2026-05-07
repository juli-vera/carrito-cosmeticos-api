# API REST - Carrito de Compras de Cosméticos

## Descripción

Este proyecto consiste en el desarrollo de una API REST utilizando Flask para gestionar un carrito de compras de cosméticos.

La aplicación permite:

* Listar productos
* Agregar productos al carrito
* Ver el contenido del carrito
* Eliminar productos del carrito
* Calcular el total de la compra
* Vaciar el carrito

La persistencia se realiza en memoria, sin utilizar base de datos.

---

# Tecnologías utilizadas

* Python
* Flask
* Flasgger (Swagger)
* unittest

---

# Instalación

## 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
```

## 2. Entrar a la carpeta del proyecto

```bash
cd cosmeticos
```

## 3. Crear entorno virtual

```bash
python -m venv .venv
```

## 4. Activar entorno virtual

### Windows

```bash
.venv\Scripts\activate
```

---

# Instalar dependencias

```bash
pip install flask flasgger
```

---

# Ejecutar la aplicación

```bash
python app.py
```

La API se ejecutará en:

```text
http://localhost:5000
```

---

# Documentación Swagger

La documentación interactiva de la API se encuentra en:

```text
http://localhost:5000/apidocs
```

Desde Swagger es posible probar todos los endpoints.

---

# Endpoints principales

## Obtener productos

```http
GET /products
```

Devuelve la lista de productos disponibles.

---

## Ver carrito

```http
GET /cart
```

Devuelve los productos agregados al carrito.

---

## Agregar producto al carrito

```http
POST /cart/items
```

Ejemplo de body:

```json
{
  "product_id": 1,
  "quantity": 2
}
```

---

## Eliminar producto del carrito

```http
DELETE /cart/items/{product_id}
```

---

## Obtener total del carrito

```http
GET /cart/total
```

---

## Vaciar carrito

```http
DELETE /cart
```

---

# Tests unitarios

Los tests fueron realizados utilizando unittest.

Para ejecutarlos:

```bash
python test_app.py
```

---

# Estructura del proyecto

```text
cosmeticos/
│
├── app.py
├── cart.py
├── products.py
├── test_app.py
├── requirements.txt
└── README.md
```

---

# Autor

Proyecto realizado para la materia de Programación Web.
