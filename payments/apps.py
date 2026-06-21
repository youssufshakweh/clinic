from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    name = 'payments'

    def ready(self):
        from core.admin import autoregister
        autoregister('payments')
        import payments.signals  # noqa: F401
