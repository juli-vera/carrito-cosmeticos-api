from app import app as flask_app
from database import init_db
import os
import sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
os.environ["DB_PATH"] = ":memory:"


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    init_db()
    with flask_app.test_client() as c:
        c.delete("/cart")
        yield c


def test_get_products_returns_8(client):
    r = client.get("/products")
    assert r.status_code == 200
    assert len(r.get_json()) == 8


def test_products_have_required_fields(client):
    for p in client.get("/products").get_json():
        assert "id" in p and "name" in p and "price" in p


def test_cart_empty_initially(client):
    assert client.get("/cart").get_json() == []


def test_add_item_to_cart(client):
    client.post("/cart/items", json={"product_id": 1, "quantity": 1})
    cart = client.get("/cart").get_json()
    assert len(cart) == 1 and cart[0]["product_id"] == 1


def test_add_same_item_increments_quantity(client):
    client.post("/cart/items", json={"product_id": 1, "quantity": 1})
    client.post("/cart/items", json={"product_id": 1, "quantity": 1})
    assert client.get("/cart").get_json()[0]["quantity"] == 2


def test_add_invalid_product_returns_404(client):
    assert client.post(
        "/cart/items", json={"product_id": 999}).status_code == 404


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
