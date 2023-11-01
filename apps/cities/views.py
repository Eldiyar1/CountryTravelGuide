from rest_framework import viewsets, status, response, generics, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from ..users import models as users

from .models import Region, City, Kitchen, Image, Menu, Rating, Review
from .serializers import RegionSerializer, CitySerializer, KitchenSerializer, ImageSerializer, MenuSerializer, \
    EventSerializer, ReviewSerializer
from .permissions import OnlyGet, KitchenPermission, MenuPermission
from .utils import calculate_file_hash, get_client_ip


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        image_file = request.data.get('image')
        if request.user.is_authenticated:
            if image_file:
                image_hash = calculate_file_hash(image_file)
                existing_image = Image.objects.filter(hash=image_hash).first()

                if existing_image:
                    serializer = ImageSerializer(existing_image)
                    return response.Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    image = Image(image=image_file, hash=image_hash)
                    image.image_path = image.image.url
                    image.save()
                    serializer = ImageSerializer(image)
                    return response.Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return response.Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return response.Response({'error': 'You need to authenticate'}, status=status.HTTP_403_FORBIDDEN)


class RegionsViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [OnlyGet]

    @action(detail=True, methods=['GET'], url_path='get-cities')
    def get_cities(self, request, pk):
        cities = City.objects.filter(city_region_id=pk)
        serializer = CitySerializer(cities, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [OnlyGet]

    @action(detail=True, methods=['POST'], url_path='subscribe')
    def subscribe(self, request, pk):
        city = City.objects.get(id=pk)
        if request.user.is_authenticated:
            city.subscribers.add(request.user)
            city.save()
            return response.Response({"detail": f"You subscribed as {request.user.username}"}, status=status.HTTP_200_OK)
        ip_address = get_client_ip(request)
        session_key = request.session.session_key
        if session_key:
            anonymous, created = users.AnonymousUser.objects.get_or_create(ip_address=ip_address)
            anonymous.session_key = session_key
            city.anonymous_subscribers.add(anonymous)
            city.save()
            return response.Response({"detail": "You subscribed as anonymous user"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'], url_path='get-reviews')
    def get_reviews(self, request, region_pk, pk):
        city = City.objects.get(id=pk)
        return response.Response(ReviewSerializer(Review.objects.filter(city=city), many=True).data,
                                 status=status.HTTP_200_OK)
    

class KitchenViewSet(viewsets.ModelViewSet):
    serializer_class = KitchenSerializer
    permission_classes = [KitchenPermission]

    def perform_create(self, serializer):
        city_id = self.kwargs['city_pk']
        serializer.save(city_kitchen_id=city_id)

    def get_queryset(self):
        city_id = self.kwargs['city_pk']
        return Kitchen.objects.filter(city_kitchen__id=city_id)

    @action(detail=True, methods=['POST'], url_path='add-rating')
    def add_rating(self, request, city_pk, region_pk, pk):
        kitchen = self.get_object()
        rating_value = request.data.get('value')
        if rating_value is not None:
            if request.user.is_authenticated:
                rating, created = Rating.objects.get_or_create(user=request.user, value=rating_value, kitchen=kitchen)
                if not created:
                    return response.Response({"detail": "Вы уже голосовали"})
                rating.save()
                kitchen.ratings.add(rating)
                kitchen.save()
                return response.Response({"detail": "Рейтинг успешно добавлен"}, status=status.HTTP_201_CREATED)
            else:
                ip_address = get_client_ip(request)
                session_key = request.session.session_key
                if session_key:
                    anonymous, created = users.AnonymousUser.objects.get_or_create(ip_address=ip_address)
                    anonymous.session_key = session_key
                    rating = Rating.objects.create(anonymous=anonymous, value=rating_value, kitchen=kitchen)
                    rating.save()
                    kitchen.ratings.add(rating)
                    kitchen.save()
                    return response.Response({"detail": "Рейтинг успешно добавлен"}, status=status.HTTP_201_CREATED)
                return response.Response({"detail": "You have no session key, must be a tester"})
        return response.Response({"detail": "Неправильный запрос"}, status=status.HTTP_400_BAD_REQUEST)


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    permission_classes = [MenuPermission]

    def get_queryset(self):
        kitchen_id = self.kwargs['kitchen_pk']
        return Menu.objects.filter(kitchen_id=kitchen_id)

    def perform_create(self, serializer):
        kitchen_id = self.kwargs['kitchen_pk']
        serializer.save(kitchen_id=kitchen_id)


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [AllowAny]


