from rest_framework import serializers
from cart.models import Cart
from shop.serializers import ShopSerializers
from product.serializers import ProductSerializers


class CartSerializers(serializers.ModelSerializer):
    shop = ShopSerializers(read_only=True)
    product = ProductSerializers(read_only=True)
    class Meta:
        model = Cart
        fields = ['uid','shop','product','quantity']


class AddCartSerializers(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['shop','product','quantity']


class CartProduct(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['product']