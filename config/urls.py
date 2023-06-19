"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from account_api.views import UserRegistrationView,UserLoginView,UserProfileView,UserChangePasswordView,SendPasswordResetEmailView,UserPasswordResetView,UserList

from category.views import CategoryList,CategoryDetail

from shop.views import ShopAPIView,ShopListView,ShopDetailView,ShopStatusView

from product.views import ProductAPIView, ProductDetailView ,ProductSearchView, ConnectedShopProduct

from connection.views import SendConnectionView,ConnectionRequest,ConnectionRequestAction,ConnectedShopView

from cart.views import CartList

from order.views import OrderApiView

urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('api/schema', SpectacularAPIView.as_view(), name='api-schema'),
    path('admin', admin.site.urls),
    # # authentication app url
    # path('api/auth/',include('account_api.urls')),
    # # category app url
    # path('api/',include('category.urls')),
    # # shop app url 
    # path('api/',include('shop.urls')),
    # # product app url 
    # path('api/shops/<shop_uid>/',include('product.urls')),
    # # connection app url 
    # path('api/connections/',include('connection.urls')),
    # # cart app url 
    # path('api/shops/<shop_uid>/',include('cart.urls')),
    # # order app url 
    # path('api/shops/<shop_uid>/',include('order.urls')),

    # Authentication app url
    path('auth/register',UserRegistrationView.as_view()),
    path('auth/login',UserLoginView.as_view()),
    path('auth/change-password',UserChangePasswordView.as_view()),
    path('auth/reset-password',SendPasswordResetEmailView.as_view()),
    path('auth/reset-password/<uid>/<token>',UserPasswordResetView.as_view()),

    # Profile url
    path('profile',UserProfileView.as_view()),

    # User List
    path('users',UserList.as_view()),

    # Categories app url 
    path('categories',CategoryList.as_view()),
    path('categories/<uid>',CategoryDetail.as_view()),

    # shop app url 
    path('organizations',ShopListView.as_view()),
    path('we/organizations',ShopAPIView.as_view()),
    path('we/organizations/<uid>',ShopDetailView.as_view()),
    path('we/organizations/<uid>/<status>', ShopStatusView.as_view()),

    # product app url 
    path('organizations/<uid>/products/search',ProductSearchView.as_view()),
    path('organizations/<org_uid>/products/<uid>',ProductDetailView.as_view()),
    path('organizations/<uid>/products',ProductAPIView.as_view()),
  

    # connection app url 
    path('connections/send/<target_org>',SendConnectionView.as_view()),
    path('connections/request',ConnectionRequest.as_view()),
    path('connections/<uid>/status',ConnectionRequestAction.as_view()),
    path('connections/connected-org/<uid>',ConnectedShopView.as_view()),
    path('connections/organizations/<uid>/products',ConnectedShopProduct.as_view()),

    # cart app url 
    path('organizations/<uid>/carts',CartList.as_view()),

    # order app url 
    path('organizations/<uid>/orders',OrderApiView.as_view()),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
