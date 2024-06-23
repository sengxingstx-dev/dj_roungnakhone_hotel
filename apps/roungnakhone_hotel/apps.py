from django.apps import AppConfig


class RoungnakhoneHotelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.roungnakhone_hotel'

    def ready(self):
        from . import signals
