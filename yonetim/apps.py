from django.apps import AppConfig


class YonetimConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "yonetim"

    def ready(self):
        pass
