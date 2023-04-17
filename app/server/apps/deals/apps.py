from django.apps import AppConfig


class DealsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.deals'

    def ready(self):
        import server.api.deals.signals
