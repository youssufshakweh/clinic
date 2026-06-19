from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend

from .models import Inquiry
from .serializers import InquirySerializer, ContactReplySerializer
from .services import reply_to_inquiry
from utils.pagination import StandardPagination


class ContactViewSet(viewsets.ModelViewSet):
    http_method_names = ["get", "post"]

    queryset = Inquiry.objects.all().order_by('is_read', '-created_at')
    serializer_class = InquirySerializer
    pagination_class = StandardPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_read']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    @extend_schema(request=ContactReplySerializer, responses=inline_serializer("MessageResponse", {"message": serializers.CharField()}))
    @action(detail=True, methods=['post'])
    def reply(self, request, pk=None):
        contact = self.get_object()
        serializer = ContactReplySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            contact = reply_to_inquiry(contact, **serializer.validated_data)
        except Exception as e:
            raise serializers.ValidationError({
                "detail": f"Failed to send email to {contact.email}: {str(e)}"
            })

        return Response({"message": "تم إرسال الرد بنجاح"})


