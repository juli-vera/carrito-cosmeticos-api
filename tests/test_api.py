from app import app as flask_app
from database import init_db
import os  # importa funciones del sistema operativo, modifica variables de entorno
import sys  # modifica como python busca los achivos
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
# Para que SQLite use una base de datos en memoria, usa RAM
os.environ["DB_PATH"] = ":memory:"


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    init_db()
    with flask_app.test_client() as c:
        c.delete("/cart")
        yield c  # Entrega el cliente al test


def test_get_products_returns_8(client):
    r = client.get("/products")
    assert r.status_code == 200
    assert len(r.get_json()) == 8


def test_products_have_required_fields(client):
    respuesta = client.get("/products")
    productos = respuesta.get_json()
    for producto in productos:
        assert "id" in producto
        assert "name" in producto
        assert "price" in producto


def test_cart_empty_initially(client):
    assert client.get("/cart").get_json() == []


def test_add_item_to_cart(client):
    client.post("/cart/items", json={"product_id": 1, "quantity": 1})
    cart = client.get("/cart").get_json()
    assert len(cart) == 1
    assert cart[0]["product_id"] == 1


def test_add_same_item_increments_quantity(client):
    client.post("/cart/items", json={"product_id": 1, "quantity": 1})
    client.post("/cart/items", json={"product_id": 1, "quantity": 1})
    assert client.get("/cart").get_json()[0]["quantity"] == 2


def test_add_invalid_product_returns_404(client):
    respuesta = client.post(
        "/cart/items", json={"product_id": 999})
    assert respuesta.status_code == 404


def test_add_missing_product_id_returns_400(client):
    assert client.post("/cart/items", json={"quantity": 1}).status_code == 400


def test_add_negative_quantity_returns_400(client):
    assert client.post(
        "/cart/items", json={"product_id": 1, "quantity": -1}).status_code == 400


def test_remove_item_from_cart(client):
    client.post("/cart/items", json={"product_id": 1, "quantity": 1})
    assert client.delete("/cart/items/1").status_code == 200
    assert client.get("/cart").get_json() == []


def test_remove_nonexistent_item_returns_404(client):
    assert client.delete("/cart/items/1").status_code == 404


def test_total_is_correct(client):
    client.post("/cart/items", json={"product_id": 1, "quantity": 1})
    client.post("/cart/items", json={"product_id": 2, "quantity": 2})
    assert client.get("/cart/total").get_json()["total"] == 13420


def test_clear_cart(client):
    client.post("/cart/items", json={"product_id": 1, "quantity": 1})
    client.delete("/cart")
    assert client.get("/cart").get_json() == []
