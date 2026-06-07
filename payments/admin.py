from django.contrib import admin
from .models import Payment, Cart, CartItem, Order, OrderItem

for model in [Payment, Cart, CartItem, Order, OrderItem]:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
