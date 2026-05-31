from django.apps import apps
from django.contrib import admin


def autoregister(app_name):
    app_config = apps.get_app_config(app_name)
    
    for model in app_config.get_models():
        if not admin.site.is_registered(model):
            admin.site.register(model)