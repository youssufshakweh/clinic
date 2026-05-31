from django.apps import AppConfig


class NutritionistsConfig(AppConfig):
    name = 'nutritionists'

    def ready(self):
        from core.admin import autoregister
        autoregister('nutritionists')
