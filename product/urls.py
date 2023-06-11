from django.urls import path
from product.views import ProductAPIView, ProductDetailView ,ProductSearchView, ConnectedShopProduct

urlpatterns = [
    path('products/search',ProductSearchView.as_view()),
    path('products/<product_uid>',ProductDetailView.as_view()),
    path('products',ProductAPIView.as_view()),
    path('connected-shops/products',ConnectedShopProduct.as_view())
]