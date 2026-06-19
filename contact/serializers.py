from rest_framework import serializers
from .models import Inquiry


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = [
            'id', 'name', 'email', 'phone', 'message', 'created_at',
            'is_read', 'reply', 'replied_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_read', 'reply', 'replied_at']


class ContactReplySerializer(serializers.Serializer):
    reply = serializers.CharField(allow_blank=False, min_length=1)
    subject_title = serializers.CharField(allow_blank=False, min_length=1)
