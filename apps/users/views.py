from django.contrib.auth import authenticate, hashers
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.utils import timezone

from .utils import send_email_confirm, get_client_ip, confirmation_code, send_email_reset_password, recovery_code
from .models import User, Notification, AnonymousUser, PasswordResetToken
from .serializer import RegisterSerializer, LoginSerializer, ConfirmSerializer, PasswordResetSerializer, \
    PasswordResetCodeSerializer, PasswordResetNewPasswordSerializer
from .permissions import NotificationPermission


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
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            user = User.objects.filter(email=email).first()

            if not user:
                return Response({'error': 'Неверный email.'}, status=400)

            if user.code != code:
                return Response({'error': 'Неверный код подтверждения.'}, status=400)

            user.code = None
            user.is_active = True
            user.save()

            return Response({'message': 'Аккаунт успешно подтвержден.'}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(CreateAPIView):
    serializer_class = PasswordResetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        try:
            send_email_reset_password(email=email)
            return Response({"message": "Password reset email sent successfully."}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)


class PasswordResetCodeAPIView(CreateAPIView):
    serializer_class = PasswordResetCodeSerializer

    def create(self, request, password=None, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        code = serializer.validated_data.get("code")

        try:
            password_reset_token = PasswordResetToken.objects.get(
                code=code, time__gt=timezone.now()
            )
            user = password_reset_token.user
            user.password = hashers.make_password(password)
            user.save()
            return Response(data={"message": "success", "code": code}, status=status.HTTP_200_OK)
        except PasswordResetToken.DoesNotExist:
            return Response(
                status=status.HTTP_406_NOT_ACCEPTABLE,
                data={"error": "Недействительный код для сброса пароля или время истечения кода закончилось."},
            )


class PasswordResetNewPasswordAPIView(CreateAPIView):
    serializer_class = PasswordResetNewPasswordSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = kwargs["code"]
            password = serializer.validated_data["password"]

            try:
                password_reset_token = PasswordResetToken.objects.get(
                    code=code, time__gt=timezone.now()
                )
            except PasswordResetToken.DoesNotExist:
                return Response(
                    data={"detail": "Недействительный код для сброса пароля или время истечения кода закончилось."},
                    status=status.HTTP_400_BAD_REQUEST)

            user = password_reset_token.user
            user.password = hashers.make_password(password)
            user.save()

            password_reset_token.delete()
            return Response(data={"detail": "Пароль успешно обновлен"}, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
