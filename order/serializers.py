from rest_framework import serializers
from order.models import Order
from shop.serializers import ShopSerializers


class OrderSerializers(serializers.ModelSerializer):
    shop = ShopSerializers(read_only=True)

    class Meta:
        model = Order
        fields = ['uid','shop','product','total_price','order_status']


class OrderPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['shop','product','total_price']