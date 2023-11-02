from django.urls import path, include
from rest_framework_nested import routers
from .views import RegionsViewSet, CityViewSet, KitchenViewSet, ImageViewSet, MenuViewSet, EventViewSet

router = routers.DefaultRouter()
router.register('region', RegionsViewSet, basename='region')
router.register('image', ImageViewSet, basename='image')

region_router = routers.NestedSimpleRouter(router, r'region', lookup='region')
region_router.register('city', CityViewSet, basename='city')

city_router = routers.NestedSimpleRouter(region_router, r'city', lookup='city')
city_router.register('kitchen', KitchenViewSet, basename='kitchen')
city_router.register('event', EventViewSet, basename='event')

kitchen_router = routers.NestedSimpleRouter(city_router, r'kitchen', lookup='kitchen')
kitchen_router.register('menu', MenuViewSet, basename='menu')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(region_router.urls)),
    path('', include(city_router.urls)),
    path('', include(kitchen_router.urls)),
]
