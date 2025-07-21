from rest_framework import generics, permissions
from django.core.cache import cache
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer, CartItemSerializer
from common.kafka_producer import send_kafka_message

class CartView(generics.RetrieveAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        cart_key = f'cart_{user.id}'
        cart = cache.get(cart_key)

        if cart is None:
            cart, created = Cart.objects.get_or_create(user=user)
            # Cache the cart for 5 minutes (300 seconds)
            cache.set(cart_key, cart, 300)
        return cart

class AddToCartView(generics.CreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)
        product_id = self.request.data.get('product_id')
        quantity = self.request.data.get('quantity', 1)
        product = Product.objects.get(id=product_id)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': quantity})
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        serializer.instance = cart_item
        # Invalidate the cache for this user's cart
        cache.delete(f'cart_{user.id}')
        send_kafka_message('cart_item_added', {
            'user_id': user.id,
            'product_id': product.id,
            'quantity': cart_item.quantity,
            'cart_item_id': cart_item.id,
            'action': 'added' if created else 'updated'
        })
