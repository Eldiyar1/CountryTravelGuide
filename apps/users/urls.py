from django.urls import path
from .views import RegisterAPIView, LoginAPIView, ConfirmAPIView, \
    PasswordResetAPIView, PasswordResetCodeAPIView, PasswordResetNewPasswordAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('confirm/', ConfirmAPIView.as_view()),
    # URL-путь для ввода кода подтверждения
    path('password/reset/code/', PasswordResetAPIView.as_view()),
    # URL-путь для установки нового пароля
    path('password/reset/new/', PasswordResetCodeAPIView.as_view()),
    path('password/reset/password/<str:code>/', PasswordResetNewPasswordAPIView.as_view()),

]
