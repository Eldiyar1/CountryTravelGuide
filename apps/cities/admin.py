from django.contrib import admin
from .models import Region, City, Image, Hotel, Event, Kitchen, Attraction, Menu


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['title', 'city_region']


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['image']


@admin.register(Hotel, Event, Attraction)
class Motion(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'city_kitchen']


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

