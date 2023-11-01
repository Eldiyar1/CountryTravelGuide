from rest_framework import serializers
from .models import Region, City, Kitchen, Image, Menu


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = '__all__'
        read_only_fields = ('city_kitchen',)


class ImageSerializer(serializers.ModelSerializer):
    image_path = serializers.CharField(source='image.url', read_only=True)

    class Meta:
        model = Image
        fields = ('id', 'image', 'hash', 'image_path')


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ('kitchen',)