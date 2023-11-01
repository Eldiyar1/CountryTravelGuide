from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .utils import send_email_confirm
from .models import User
from .serializer import RegisterSerializer, LoginSerializer, ConfirmSerializer


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            send_email_confirm(user.email)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(CreateAPIView):
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():

            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(username=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                access = AccessToken.for_user(user)
                return Response({
                    'message': 'Пользователь успешно аутентифицирован.',
                    "status": status.HTTP_200_OK,
                    "refresh_token": str(refresh),
                    "access_token": str(access)
                })
            return Response({'message': 'Ошибка аутентификации. Пожалуйста, проверьте введенные данные.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmAPIView(CreateAPIView):
    serializer_class = ConfirmSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data('email')
            code = serializer.validated_data('code')

            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'error': 'Неверный email.'}, status=400)

            if user.code != code:
                return Response({'error': 'Неверный код подтверждения.'}, status=400)

            user.is_active = True
            user.save()

            return Response({'message': 'Аккаунт успешно подтвержден.'}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
