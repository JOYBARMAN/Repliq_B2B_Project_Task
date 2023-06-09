from django.urls import path
from connection.views import SendConnectionView,ConnectionRequest,ConnectionRequestAction,ConnectedShopView

urlpatterns = [
    path('send/<target_shop_uid>',SendConnectionView.as_view()),
    path('request',ConnectionRequest.as_view()),
    path('<connection_uid>/action',ConnectionRequestAction.as_view()),
    path('shops/<shop_uid>',ConnectedShopView.as_view())
]