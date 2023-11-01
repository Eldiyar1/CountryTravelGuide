# Generated by Django 4.2.6 on 2023-11-01 22:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cities', '0003_rating_anonymous_rating_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kitchen',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='kitchen',
            name='menu',
            field=models.ManyToManyField(blank=True, null=True, to='cities.menu'),
        ),
        migrations.AlterField(
            model_name='kitchen',
            name='phone_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='kitchen',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
    ]
