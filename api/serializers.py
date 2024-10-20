from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')
    
    class Meta:
        model = Order
        fields = '__all__'

class PlaceOrder(serializers.ModelSerializer):
    product = serializers.CharField(source='product__OrderItem')
    quantity = serializers.CharField(source='quantity__OrderItem')
    price = serializers.CharField(source='price__OrderItem')

    class Meta:
        model = Order
        fields = ('total_price', 'status', 'product', 'quantity', 'price')
