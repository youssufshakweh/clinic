from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    name = 'notifications'
    def ready(self):
        import notifications.signals

        from core.admin import autoregister
        autoregister('notifications')