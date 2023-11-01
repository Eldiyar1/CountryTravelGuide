from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from .utils import send_email_confirm, get_client_ip
from .models import User, Notification, AnonymousUser
from .serializer import RegisterSerializer, LoginSerializer, ConfirmSerializer, NotificationSerializer
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

            user.is_active = True
            user.save()

            return Response({'message': 'Аккаунт успешно подтвержден.'}, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationView(APIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [NotificationPermission]

    def get(self, request):
        if self.request.user.is_authenticated:
            user = self.request.user
            notifications = Notification.objects.filter(user=user)
            return Response(NotificationSerializer(notifications, many=True).data, status=status.HTTP_200_OK)
        else:
            ip_address = get_client_ip(request)
            session_key = request.session.session_key
            if session_key:
                anonymous, created = AnonymousUser.objects.get_or_create(ip_address=ip_address)
                anonymous.session_key = session_key
                return Response(NotificationSerializer(Notification.objects.filter(anonymous_user=anonymous)).data,
                                status=status.HTTP_404_NOT_FOUND)
            return Response({"detail": "You have no session key, must be a tester"})
