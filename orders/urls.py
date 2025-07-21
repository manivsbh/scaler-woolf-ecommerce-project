
from django.urls import path
from .views import OrderCreateView, OrderListView, PaymentProcessView

urlpatterns = [
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),
    path('payments/process/', PaymentProcessView.as_view(), name='payment-process'),
]
