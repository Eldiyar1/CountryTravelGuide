import random

from django.conf import settings
from django.core.mail import send_mail

from .models import User


def send_email_confirm(email):
    subject = 'Подтверждение регистрации'
    random_code = random.randint(100000, 999999)
    message = f"""Здравствуйте! Ваш адрес электронной почты был указан для входа на приложение Country Travel Guide. 
    Пожалуйста, введите этот код на странице авторизации:<<< {random_code} >>> 
    Если это не вы или вы не регистрировались на сайте, то просто проигнорируйте это письмо"""
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
    user_obj = User.objects.get(email=email)
    user_obj.code = random_code
    user_obj.save()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip