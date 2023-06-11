from django.urls import path
from cart.views import CartList

urlpatterns = [
    path('carts',CartList.as_view()),
]