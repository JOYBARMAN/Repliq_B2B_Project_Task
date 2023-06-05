from django.urls import path
from product.views import ProductAPIView, ProductDetailView ,ProductSearchView

urlpatterns = [
    path('allproduct/',ProductAPIView.as_view()),
    path('product/<product_uid>/',ProductDetailView.as_view()),
    path('product_search/',ProductSearchView.as_view()),
]