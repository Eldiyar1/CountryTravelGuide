# Generated by Django 4.2.6 on 2023-11-01 20:38

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0004_notification_anonymous_user_alter_notification_user'),
        ('cities', '0002_alter_menu_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='anonymous_subscribers',
            field=models.ManyToManyField(blank=True, to='users.anonymoususer'),
        ),
        migrations.AddField(
            model_name='city',
            name='subscribers',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
