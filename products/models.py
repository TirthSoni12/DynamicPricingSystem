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


class Discount(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def apply_discount(self, price):
        raise NotImplementedError("Subclasses must implement this method")

    class Meta:
        abstract = True


class PercentageDiscount(Discount):
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def apply_discount(self, price):
        return price * (1 - self.percentage / 100)


class FixedAmountDiscount(Discount):
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def apply_discount(self, price):
        return max(0, price - self.amount)


class Order(models.Model):
    products = models.ManyToManyField(Product, through='OrderItem')

    def calculate_total(self):
        total = 0
        for item in self.orderitem_set.all():
            price = item.product.get_price(quantity=item.quantity)
            if item.discount:
                price = item.discount.apply_discount(price)
            total += price * item.quantity
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
