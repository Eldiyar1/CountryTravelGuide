# Generated by Django 4.2.3 on 2023-11-01 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.CharField(max_length=4, null=True, verbose_name='Код подтверждения'),
        ),
    ]