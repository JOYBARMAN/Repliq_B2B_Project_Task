from django.urls import path
from shop.views import ShopAPIView,ShopDetailView,ActiveShopView,DeactiveShopView

urlpatterns = [
    path('all/',ShopAPIView.as_view()),
    path('detail/<uid>/',ShopDetailView.as_view()),
    path('active/<shop_uid>/',ActiveShopView.as_view()),
    path('deactive/<shop_uid>/',DeactiveShopView.as_view())
]
