from datetime import datetime

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def get_price(self):
        return self.price

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class SeasonalProduct(Product):
    start_date = models.DateField()
    end_date = models.DateField()
    discount_percentage = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def get_price(self):
        today = datetime.now().date()
        if self.start_date <= today <= self.end_date:
            return self.price * (1 - self.discount_percentage / 100)
        return self.price


class BulkProduct(Product):
    bulk_quantity = models.PositiveIntegerField()
    bulk_discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def get_price(self, quantity=1):
        if quantity >= self.bulk_quantity:
            return self.price * (1 - self.bulk_discount_percentage / 100)
        return self.price
