from rest_framework import serializers
from product.models import Product
from shop.serializers import ShopSerializers


class ProductSerializers(serializers.ModelSerializer):
    organization = ShopSerializers(read_only=True)

    class Meta:
        model = Product
        fields = ["uid", "organization", "product_name","price", "description", "image"]

class ProductPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["organization", "product_name","price", "description", "image"]
