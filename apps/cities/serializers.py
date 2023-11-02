from rest_framework import serializers
from .models import Region, City, Kitchen, Image, Menu, Event, Rating, Review


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = '__all__'


class KitchenSerializer(serializers.ModelSerializer):
    ratings = serializers.SerializerMethodField()

    def get_ratings(self, obj):
        ratings = obj.kitchen_rating.all()
        if ratings:
            total_rating = sum(rating.value for rating in ratings)
            average_rating = total_rating / len(ratings)
            return average_rating
        return 0

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


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
