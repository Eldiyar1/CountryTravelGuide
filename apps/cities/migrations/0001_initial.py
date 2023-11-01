# Generated by Django 4.2.6 on 2023-11-01 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Base',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('descriptions', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('hash', models.CharField(blank=True, max_length=32, null=True, unique=True)),
                ('image_path', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cities.base')),
            ],
            bases=('cities.base',),
        ),
        migrations.CreateModel(
            name='Kitchen',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cities.base')),
                ('city_kitchen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_kitchen', to='cities.city')),
            ],
            bases=('cities.base',),
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cities.base')),
                ('regional_specialties', models.TextField()),
            ],
            bases=('cities.base',),
        ),
        migrations.AddField(
            model_name='base',
            name='images',
            field=models.ManyToManyField(to='cities.image'),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('price', models.PositiveIntegerField()),
                ('images', models.ManyToManyField(blank=True, null=True, to='cities.image')),
                ('kitchen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kitchen_menu', to='cities.kitchen')),
            ],
        ),
        migrations.AddField(
            model_name='kitchen',
            name='menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='menus', to='cities.menu'),
        ),
        migrations.AddField(
            model_name='kitchen',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cities.base')),
                ('city_hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_hotel', to='cities.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            bases=('cities.base',),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cities.base')),
                ('city_event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_event', to='cities.city')),
            ],
            bases=('cities.base',),
        ),
        migrations.AddField(
            model_name='city',
            name='city_region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_region', to='cities.region'),
        ),
        migrations.CreateModel(
            name='Attraction',
            fields=[
                ('base_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cities.base')),
                ('city_attr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city_attr', to='cities.city')),
            ],
            bases=('cities.base',),
        ),
    ]