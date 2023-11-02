from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from django_resized import ResizedImageField

from apps.users.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    phone_number = PhoneNumberField(verbose_name="Номер телефона")
    birth_date = models.DateField(null=True, verbose_name="Дата рождения")
    image = ResizedImageField(upload_to='', size=(500, 300))
    email = models.EmailField(max_length=50, null=True, unique=True, verbose_name="почта")
    password = models.CharField(max_length=100, verbose_name="Пароль")
    is_active = models.BooleanField(default=False, verbose_name="Активен")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")
    is_superuser = models.BooleanField(default=False, verbose_name="Суперпользователь")
    code = models.CharField(max_length=4, null=True, verbose_name='Код подтверждения')
    is_hotel = models.BooleanField(default=False)
    is_kitchen = models.BooleanField(default=False)
    editor = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name', 'password')

    objects = UserManager()

    class Meta:
        app_label = 'users'
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.email}'


class AnonymousUser(models.Model):
    ip_address = models.GenericIPAddressField()
    session_key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.session_key


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    anonymous_user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=100)
    time = models.DateTimeField()
