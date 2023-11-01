from django.db import models
from ..users import models as users


class Base(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.TextField(null=True, blank=True)
    images = models.ManyToManyField('Image')

    def __str__(self):
        return self.title


class Image(models.Model):
    user = models.ForeignKey(users.User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    hash = models.CharField(max_length=32, unique=True, null=True, blank=True)
    image_path = models.CharField(max_length=255)

    def __str__(self):
        return self.image.name


class Region(Base):
    regional_specialties = models.TextField()


class City(Base):
    city_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='city_region')


class Hotel(Base):
    user = models.ForeignKey(users.User, on_delete=models.CASCADE)
    city_hotel = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_hotel')


class Menu(models.Model):
    kitchen = models.ForeignKey('Kitchen', on_delete=models.CASCADE, related_name='kitchen_menu')
    name = models.CharField(max_length=255)
    description = models.TextField()
    images = models.ManyToManyField(Image, null=True, blank=True)
    price = models.PositiveIntegerField()


class Kitchen(Base):
    user = models.ForeignKey(users.User, on_delete=models.SET_NULL, null=True, blank=True)
    city_kitchen = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_kitchen')
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menus', null=True, blank=True)


class Event(Base):
    city_event = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_event')


class Attraction(Base):
    city_attr = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_attr')

