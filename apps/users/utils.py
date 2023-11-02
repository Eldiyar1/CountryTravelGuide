import random
import secrets

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
from .models import PasswordResetToken

from .models import User

confirmation_code = random.randint(1000, 9999)
recovery_code = secrets.token_urlsafe(4)

def send_email_confirm(email):
    subject = 'Подтверждение регистрации'
    message = f"""Здравствуйте! Ваш адрес электронной почты был указан для входа на приложение Country Travel Guide. 
    Пожалуйста, введите этот код на странице авторизации:<<< {confirmation_code} >>> 
    Если это не вы или вы не регистрировались на сайте, то просто проигнорируйте это письмо"""
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
    user_obj = User.objects.get(email=email)
    user_obj.code = confirmation_code
    user_obj.save()


def send_email_reset_password(email):
    user = User.objects.get(email=email)
    code = get_random_string(length=4, allowed_chars='0123456789')
    time = timezone.now() + timezone.timedelta(minutes=5)

    PasswordResetToken.objects.create(user=user, code=code, time=time)

    subject = "Восстановление пароля"
    message = f"Код для восстановления пароля: <<< {code} >>> Код действителен в течение 5 минут"
    email_from = settings.EMAIL_HOST_USER
    send_mail(subject, message, email_from, [email])


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip