from rest_framework import viewsets, status, response, generics, mixins
from rest_framework.decorators import action
from ..users import models as users

from .models import Region, City, Kitchen, Image, Menu
from .serializers import RegionSerializer, CitySerializer, KitchenSerializer, ImageSerializer, MenuSerializer
from .permissions import OnlyGet, KitchenPermission, MenuPermission
from .utils import calculate_file_hash, get_client_ip



class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        image_file = request.data.get('image')
        # if request.user.is_authenticated:
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
        # else:
        #     return response.Response({'error': 'You need to authenticate'}, status=status.HTTP_403_FORBIDDEN)


class RegionsViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [OnlyGet]


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


class KitchenViewSet(viewsets.ModelViewSet):
    serializer_class = KitchenSerializer
    permission_classes = [KitchenPermission]

    def perform_create(self, serializer):
        city_id = self.kwargs['city_pk']
        serializer.save(city_kitchen_id=city_id)

    def get_queryset(self):
        city_id = self.kwargs['city_pk']
        return Kitchen.objects.filter(city_kitchen__id=city_id)


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    permission_classes = [MenuPermission]

    def get_queryset(self):
        kitchen_id = self.kwargs['kitchen_pk']
        return Menu.objects.filter(kitchen_id=kitchen_id)

    def perform_create(self, serializer):
        kitchen_id = self.kwargs['kitchen_pk']
        serializer.save(kitchen_id=kitchen_id)


