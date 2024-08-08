from rest_framework import serializers
from .models import Product, SeasonalProduct, BulkProduct, Order, OrderItem, \
    Discount


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class SeasonalProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeasonalProduct
        fields = '__all__'


class BulkProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = BulkProduct
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
