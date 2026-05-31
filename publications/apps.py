from django.apps import AppConfig


class PublicationsConfig(AppConfig):
    name = 'publications'

    def ready(self):
        from core.admin import autoregister
        autoregister('publications')
