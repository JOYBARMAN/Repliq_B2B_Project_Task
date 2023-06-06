from rest_framework import serializers
from connection.models import Connection
from shop.serializers import ShopSerializers

class ConnectionSerializers(serializers.ModelSerializer):
    source_shop = ShopSerializers(read_only=True)
    target_shop = ShopSerializers(read_only=True)

    class Meta:
        model = Connection
        fields = ['uid','source_shop','target_shop','status']


class SendConnectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['source_shop','target_shop']


class ConnectionActionSerializers(serializers.Serializer):
    status = serializers.ChoiceField(choices=['pending','approved','rejected'])
    class Meta:
        fields = ['status']