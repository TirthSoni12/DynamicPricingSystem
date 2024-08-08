from django.test import TestCase
from .models import Product


class ProductTests(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="This is a test product.",
            price=100.00
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")

    def test_get_price(self):
        self.assertEqual(self.product.get_price(), 100.00)
