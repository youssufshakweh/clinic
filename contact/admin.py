from django.contrib import admin
from .models import Inquiry


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'is_read', 'replied_at', 'created_at']
    list_filter = ['is_read']
    search_fields = ['name', 'email']
    ordering = ['-created_at']
