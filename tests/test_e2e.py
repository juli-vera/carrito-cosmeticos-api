"""
Requiere el servidor corriendo: python app.py
Correr con: pytest tests/test_e2e.py -v
"""
import pytest
import requests
from playwright.sync_api import Page, expect

BASE = "http://localhost:5000"


@pytest.fixture(autouse=True)
def reset_cart():
    requests.delete(f"{BASE}/cart")
    yield


def add_product(page: Page, index: int = 0):
    page.locator(".add-btn").nth(index).click()
    page.wait_for_selector("#toast.show", timeout=3000)


class TestProductos:
    def test_carga_lista_de_productos(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".product-card")
        expect(page.locator(".product-card")).to_have_count(8)

    def test_cada_producto_tiene_precio(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".product-card")
        expect(page.locator(
            ".product-card").first.locator(".product-price")).to_contain_text("$")


class TestCarrito:
    def test_carrito_vacio_al_inicio(self, page: Page):
        page.goto(BASE)
        expect(page.locator(".cart-empty")).to_be_visible()

    def test_agregar_producto(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".add-btn")
        add_product(page, 0)
        expect(page.locator(".cart-item")).to_have_count(1)

    def test_badge_incrementa(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".add-btn")
        add_product(page, 0)
        expect(page.locator("#cart-count")).to_have_text("1")

    def test_mismo_producto_suma_cantidad(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".add-btn")
        add_product(page, 0)
        add_product(page, 0)
        expect(page.locator(".cart-item")).to_have_count(1)
        expect(page.locator(".cart-item-qty")).to_contain_text("2 ×")

    def test_eliminar_producto(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".add-btn")
        add_product(page, 0)
        page.locator(".remove-btn").first.click()
        page.wait_for_selector(".cart-empty", timeout=3000)
        expect(page.locator(".cart-empty")).to_be_visible()

    def test_total_visible_al_agregar(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".add-btn")
        add_product(page, 0)
        expect(page.locator("#total-amount")).to_contain_text("$")

    def test_vaciar_carrito(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".add-btn")
        add_product(page, 0)
        add_product(page, 1)
        page.locator(".btn-clear").click()
        page.wait_for_selector(".cart-empty", timeout=3000)
        expect(page.locator(".cart-empty")).to_be_visible()


class TestFlujoCompleto:
    def test_flujo_compra_completo(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".add-btn")
        add_product(page, 0)
        add_product(page, 1)
        expect(page.locator(".cart-item")).to_have_count(2)
        assert "$" in page.locator("#total-amount").inner_text()
        page.locator(".btn-checkout").click()
        page.wait_for_selector(".cart-empty", timeout=5000)
        expect(page.locator(".cart-empty")).to_be_visible()


class TestPersistencia:
    def test_carrito_persiste_al_recargar(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".add-btn")
        add_product(page, 0)
        page.reload()
        page.wait_for_selector(".cart-item", timeout=3000)
        expect(page.locator(".cart-item")).to_have_count(1)

    def test_total_persiste_al_recargar(self, page: Page):
        page.goto(BASE)
        page.wait_for_selector(".add-btn")
        add_product(page, 0)
        # Esperar a que el total este listo
        page.wait_for_function("""
            () => document.querySelector('#total-amount')?.innerText.trim().length > 0
        """)
        total_antes = page.locator("#total-amount").inner_text()
        page.reload()
        # Espera que el total vuelva a cargar
        page.wait_for_function(
            """
            () => document.querySelector('#total-amount')?.innerText.trim().length > 0
        """)
        total_despues = page.locator("#total-amount").inner_text()
        assert total_antes == total_despues
