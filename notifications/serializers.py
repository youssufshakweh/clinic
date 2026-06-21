from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'notification_id',
            'title',
            'message',
            'is_read',
            'notification_type',
            'created_at',
            'time',
        ]
        read_only_fields = [
            'notification_id',
            'title',
            'message',
            'notification_type',
            'created_at',
            'time',
        ]
