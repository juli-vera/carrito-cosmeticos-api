import sqlite3

# Nombre de la base de datos
DB_PATH = "database.db"

# Devuelve conexión a la base de datos


def get_connection():
    conexion = sqlite3.connect(DB_PATH)

    # Accede a las columnas por nombre
    conexion.row_factory = sqlite3.Row
    return conexion

# Crea las tablas e inserta productos iniciales


def init_db():
    conexion = get_connection()

    # Crea tabla de productos
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id      INTEGER PRIMARY KEY,
            name    TEXT    NOT NULL,
            price   INTEGER NOT NULL
            )
        """)
    # crea tabla carrito
    conexion.execute("""
        CREATE TABLE IF NOT EXISTS cart_items (
            product_id INTEGER PRIMARY KEY,
            quantity   INTEGER NOT NULL DEFAULT 1
        )
    """)
    conexion.commit()

    # Verifica si existen productos
    consulta = conexion.execute("SELECT COUNT(*) FROM products")
    resultado = consulta.fetchone()
    cantidad = resultado[0]

    # Si la tabla esta vacia, inserta productos
    if cantidad == 0:
        productos = [
            (1, "Mascarilla",       3800),
            (2, "Crema hidratante", 4810),
            (3, "Contorno de ojos", 9300),
            (4, "Base",            10000),
            (5, "Corrector",        8900),
            (6, "Sombra de ojos",   2600),
            (7, "Delineador",       1800),
            (8, "Labial",           5900),
        ]
        conexion.executemany(
            "INSERT INTO products VALUES (?, ?, ?)", productos)
        conexion.commit()

    conexion.close()
