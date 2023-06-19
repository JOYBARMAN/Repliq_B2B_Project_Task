from rest_framework import serializers
from shop.models import Shop
from account_api.serializers import UserProfileSerializer
from category.serializers import CategorySerializers


class ShopSerializers(serializers.ModelSerializer):
    merchant = UserProfileSerializer(read_only=True)
    category = CategorySerializers(read_only=True)

    class Meta:
        model = Shop
        fields = ['uid','merchant','organization_name','category','description','active_code','is_active']


class ShopPostSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Shop
        fields = ['merchant','organization_name','category','description','active_code']


class ActiveShopSerializer(serializers.Serializer):
    active_code = serializers.CharField(max_length=20)
    class Meta:
        fields = ['active_code']


