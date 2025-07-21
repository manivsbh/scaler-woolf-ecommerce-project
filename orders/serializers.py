
from rest_framework import serializers
from .models import Order, OrderItem, Payment
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'quantity', 'price')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'created_at', 'total_price', 'is_paid', 'items')

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'order', 'amount', 'timestamp', 'transaction_id', 'stripe_charge_id', 'stripe_payment_intent_id', 'status')
