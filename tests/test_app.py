import unittest

from app import app


class APITestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True

    def test_get_products(self):
        response = self.client.get("/products")

        self.assertEqual(response.status_code, 200)

    def test_add_to_cart(self):
        response = self.client.post(
            "/cart/items",
            json={
                "product_id": 1,
                "quantity": 2
            }
        )

        self.assertEqual(response.status_code, 200)

    def test_get_cart(self):
        self.client.post(
            "/cart/items",
            json={
                "product_id": 1,
                "quantity": 1
            }
        )

        response = self.client.get("/cart")

        self.assertEqual(response.status_code, 200)

    def test_get_total(self):
        self.client.post(
            "/cart/items",
            json={
                "product_id": 1,
                "quantity": 1
            }
        )

        response = self.client.get("/cart/total")

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
