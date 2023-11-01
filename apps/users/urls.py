from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ConfirmAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('confirm/', ConfirmAPIView.as_view()),
]
