from rest_framework import serializers
from .models import Menu, MenuImage


class MenuImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuImage
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):

    images = MenuImageSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'


