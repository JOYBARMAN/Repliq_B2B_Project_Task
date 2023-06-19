from rest_framework import serializers
from cart.models import Cart,CartItem
from shop.serializers import ShopSerializers
from product.serializers import ProductSerializers


# class CartSerializers(serializers.ModelSerializer):
#     shop = ShopSerializers(read_only=True)
#     product = ProductSerializers(read_only=True)
#     class Meta:
#         model = Cart
#         fields = ['uid','shop','product','quantity']


# class AddCartSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = ['shop','product','quantity']


class CartProduct(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product']


class CartSerializers(serializers.ModelSerializer):
    organization = ShopSerializers(read_only=True)
    class Meta:
        model = Cart
        fields = ['organization']


class CartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product','quantity','price']


class AddCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['cart','product','quantity','price']