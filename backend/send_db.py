from products_sqlite import ProductRepository

repo = ProductRepository()
repo.add_product("Mascarilla", 3800)
repo.add_product("Crema hidratante", 4810)
repo.add_product("Contorno de ojos", 9300)
repo.add_product("Base", 10000)
repo.add_product("Corrector", 8900)
repo.add_product("Sombra de ojos", 2600)
repo.add_product("Delineador", 1800)
repo.add_product("Labial", 5900)

print("Productos cargados en la base de datos")
