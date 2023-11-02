from django.apps import AppConfig


class CitiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.cities'

    def ready(self):
        import apps.cities.signals