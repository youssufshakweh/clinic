from django.apps import AppConfig


class SubscriptionsConfig(AppConfig):
    name = 'subscriptions'

    def ready(self):
        from core.admin import autoregister
        autoregister('subscriptions')
