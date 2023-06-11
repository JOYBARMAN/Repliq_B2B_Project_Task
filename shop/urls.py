from django.urls import path
from shop.views import ShopAPIView,ShopListView,ShopDetailView,ActiveShopView,DeactiveShopView

urlpatterns = [
    path('shops',ShopListView.as_view()),
    path('we/shops',ShopAPIView.as_view()),
    path('we/shops/<uid>',ShopDetailView.as_view()),
    path('shops/<shop_uid>/active',ActiveShopView.as_view()),
    path('shops/<shop_uid>/deactive',DeactiveShopView.as_view())
]
