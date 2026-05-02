from rest_framework import serializers
from .models import Order, OrderItem
from product.serializers import ProductSerializer

# 1. Used to fetch product data instead of just IDs for the panel
class MyOrderItemSerializer(serializers.ModelSerializer):    
    product = ProductSerializer() 

    class Meta:
        model = OrderItem
        fields = (
            "price",
            "product",
            "quantity",
        )

# 2. Used exclusively to display the full order list in your Management Panel API
class MyOrderSerializer(serializers.ModelSerializer):
    items = MyOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "address",
            "zipcode",
            "place",
            "phone",
            "stripe_token",
            "items",
            "paid_amount"
        )
