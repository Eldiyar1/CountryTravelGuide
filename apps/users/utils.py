import random

from django.conf import settings
from django.core.mail import send_mail

from .models import User


def send_email_confirm(email):
    subject = 'Подтверждение регистрации'
    message = f"""Здравствуйте! Ваш адрес электронной почты был указан для входа на приложение Country Travel Guide. 
    Пожалуйста, введите этот код на странице авторизации:<<< {random.randint(1000, 9999)} >>> 
    Если это не вы или вы не регистрировались на сайте, то просто проигнорируйте это письмо"""
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
    user_obj = User.objects.get(email=email)
    user_obj.code = random.randint(100000, 999999)
    user_obj.save()


