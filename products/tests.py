from datetime import datetime, timedelta

from django.test import TestCase
from .models import Product, SeasonalProduct, BulkProduct, PercentageDiscount, FixedAmountDiscount


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


class SeasonalProductTests(TestCase):

    def setUp(self):
        self.today = datetime.now().date()
        self.seasonal_product = SeasonalProduct.objects.create(
            name="Seasonal Product",
            description="This product is seasonal.",
            price=200.00,
            start_date=self.today - timedelta(days=1),
            end_date=self.today + timedelta(days=1),
            discount_percentage=20
        )

    def test_get_price_within_season(self):
        self.assertEqual(self.seasonal_product.get_price(), 160.00)

    def test_get_price_outside_season(self):
        self.seasonal_product.start_date = self.today + timedelta(days=1)
        self.seasonal_product.end_date = self.today + timedelta(days=2)
        self.seasonal_product.save()
        self.assertEqual(self.seasonal_product.get_price(), 200.00)


class BulkProductTests(TestCase):

    def setUp(self):
        # Create a bulk product
        self.bulk_product = BulkProduct.objects.create(
            name="Bulk Product",
            description="This product is for bulk purchase.",
            price=150.00,
            bulk_quantity=10,
            bulk_discount_percentage=15
        )

    def test_get_price_bulk(self):
        self.assertEqual(self.bulk_product.get_price(quantity=10), 127.50)

    def test_get_price_no_bulk_discount(self):
        self.assertEqual(self.bulk_product.get_price(quantity=5), 150.00)


class DiscountTests(TestCase):

    def setUp(self):

        self.percentage_discount = PercentageDiscount.objects.create(
            name="10% Off",
            description="10% discount",
            percentage=10
        )
        self.fixed_amount_discount = FixedAmountDiscount.objects.create(
            name="Fixed $20 Off",
            description="Fixed discount of $20",
            amount=20.00
        )

    def test_percentage_discount(self):
        self.assertEqual(self.percentage_discount.apply_discount(200.00), 180.00)

    def test_fixed_amount_discount(self):
        self.assertEqual(self.fixed_amount_discount.apply_discount(200.00), 180.00)
