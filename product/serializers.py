from rest_framework import serializers
from product.models import Product
from shop.serializers import ShopSerializers


class ProductSerializers(serializers.ModelSerializer):
    shop = ShopSerializers(read_only=True)

    class Meta:
        model = Product
        fields = ["uid", "shop", "product_name","price", "description", "image"]

class ProductPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["shop", "product_name","price", "description", "image"]
