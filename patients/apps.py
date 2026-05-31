from django.apps import AppConfig


class PatientsConfig(AppConfig):
    name = 'patients'

    def ready(self):
        from core.admin import autoregister
        autoregister('patients')