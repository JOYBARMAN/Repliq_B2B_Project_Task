from django.urls import path
from order.views import OrderApiView

urlpatterns = [
    path('orders',OrderApiView.as_view()),
]