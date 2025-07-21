
from django.urls import path
from .views import CartView, AddToCartView

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart-view'),
    path('cart/add/', AddToCartView.as_view(), name='add-to-cart'),
]
