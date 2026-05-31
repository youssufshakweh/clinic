from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'clinic'

    def ready(self):
        from core.admin import autoregister
        autoregister('clinic')