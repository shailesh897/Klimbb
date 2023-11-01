from rest_framework import serializers
from .models import Stone, Activation
from rest_framework import serializers

# ModelSerializers
class StoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stone
        fields = "__all__"


class ActivationSerializer(serializers.ModelSerializer):
    stone = StoneSerializer()

    class Meta:
        model = Activation
        fields = "__all__"



# Custome Serializers
class LoginRequestSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class ActivateRequestSerializer(serializers.Serializer):
    stone_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    power_duration = serializers.IntegerField()