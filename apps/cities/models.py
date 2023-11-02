from django.db import models
from ..users import models as users


class Base(models.Model):
    title = models.CharField(max_length=255)
    descriptions = models.TextField(null=True, blank=True)
    images = models.ManyToManyField('Image', blank=True)

    def __str__(self):
        return self.title


class Rating(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user = models.ForeignKey(users.User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous = models.ForeignKey(users.AnonymousUser, on_delete=models.CASCADE, null=True, blank=True)
    value = models.IntegerField(choices=RATING_CHOICES)
    kitchen = models.ForeignKey('Kitchen', on_delete=models.CASCADE, related_name='kitchen_rating', null=True, blank=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name='event_rating', null=True, blank=True)

    class Meta:
        unique_together = ('kitchen', 'event')

    def __str__(self):
        return str(self.value)


class Image(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    hash = models.CharField(max_length=32, unique=True, null=True, blank=True)
    image_path = models.CharField(max_length=255)

    def __str__(self):
        return self.image.name

class Specialties(Base):
    def __str__(self):
        return self.title


class Region(Base):
    regional_specialties = models.ManyToManyField(Specialties, blank=True)


class City(Base):
    city_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='city_region')
    subscribers = models.ManyToManyField(users.User, blank=True)
    anonymous_subscribers = models.ManyToManyField(users.AnonymousUser, blank=True)


class Hotel(Base):
    user = models.ForeignKey(users.User, on_delete=models.CASCADE)
    city_hotel = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_hotel')


class Menu(Base):
    price = models.PositiveIntegerField()


class Kitchen(Base):
    user = models.ForeignKey(users.User, on_delete=models.SET_NULL, null=True, blank=True)
    city_kitchen = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_kitchen')
    website = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.PositiveIntegerField(null=True, blank=True)
    menu = models.ManyToManyField(Menu, blank=True)
    ratings = models.ManyToManyField(Rating, related_name='kitchen_ratings', blank=True)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            total_rating = sum(i.value for i in ratings)
            return total_rating / len(ratings)
        return 0


class Event(Base):
    user = models.ForeignKey(users.User, on_delete=models.SET_NULL, null=True, blank=True)
    city_event = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_event')


class Attraction(Base):
    city_attr = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_attr')


class Review(models.Model):
    kitchen = models.ForeignKey(Kitchen, on_delete=models.CASCADE, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(users.User, on_delete=models.CASCADE)
    content = models.TextField()
    likes = models.IntegerField(default=0)


