from django.urls import path
from connection.views import SendConnectionView,ConnectionRequest,ConnectionRequestAction

urlpatterns = [
    path('send_connection/<target_shop_uid>/',SendConnectionView.as_view()),
    path('connection_request/',ConnectionRequest.as_view()),
    path('connection_action/<connection_uid>/',ConnectionRequestAction.as_view())
]