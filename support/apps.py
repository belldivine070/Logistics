from django.apps import AppConfig


class SupportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'support'

    def ready(self):
        # Import signals or startup hooks here if needed in the future
        pass