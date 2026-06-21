from django.contrib import admin
from .models import Notification

for model in [Notification]:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
