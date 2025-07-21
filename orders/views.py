from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.conf import settings
import stripe

from .models import Order, OrderItem, Payment
from .serializers import OrderSerializer, PaymentSerializer
from carts.models import Cart, CartItem
from common.kafka_producer import send_kafka_message

stripe.api_key = settings.STRIPE_SECRET_KEY

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        cart = Cart.objects.get(user=user)
        cart_items = cart.items.all()

        if not cart_items:
            return Response({"detail": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        order = Order.objects.create(user=user, total_price=total_price)

        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart_items.delete() # Clear the cart after creating the order

        send_kafka_message('order_created', {
            'order_id': order.id,
            'user_id': user.id,
            'total_price': str(order.total_price),
            'items': [{'product_id': item.product.id, 'quantity': item.quantity} for item in order.items.all()]
        })

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class PaymentProcessView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        order_id = request.data.get('order_id')
        payment_method_id = request.data.get('payment_method_id') # From frontend

        if not order_id or not payment_method_id:
            return Response({"detail": "Order ID and Payment Method ID are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        if order.is_paid:
            return Response({"detail": "Order already paid"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Create a PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=int(order.total_price * 100), # Amount in cents
                currency='usd',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True,
                return_url='http://localhost:8000/payment-success', # This would be your frontend success URL
                metadata={'order_id': order.id, 'user_id': request.user.id},
            )

            if payment_intent.status == 'succeeded':
                payment = Payment.objects.create(
                    order=order,
                    amount=order.total_price,
                    stripe_payment_intent_id=payment_intent.id,
                    stripe_charge_id=payment_intent.latest_charge, # Or payment_intent.charges.data[0].id
                    status='completed'
                )
                order.is_paid = True
                order.save()

                send_kafka_message('payment_processed', {
                    'order_id': order.id,
                    'payment_intent_id': payment_intent.id,
                    'amount': str(payment.amount),
                    'status': payment.status
                })

                serializer = self.get_serializer(payment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            elif payment_intent.status == 'requires_action':
                # Handle 3D Secure or other required actions
                return Response({
                    "detail": "Payment requires additional action",
                    "client_secret": payment_intent.client_secret
                }, status=status.HTTP_200_OK)
            else:
                # Handle other statuses like 'requires_confirmation', 'requires_payment_method'
                return Response({"detail": f"Payment failed with status: {payment_intent.status}"}, status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            return Response({"detail": err.get('message')}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.StripeError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
