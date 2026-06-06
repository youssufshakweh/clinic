from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import EducationalPublication
from .serializers import PublicationListSerializer, PublicationDetailSerializer
from utils.pagination import StandardPagination


class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    pagination_class = StandardPagination

    def get_queryset(self):
        return EducationalPublication.objects.filter(
            status='published'
        ).order_by('-published_at')

    def get_serializer_class(self):
        if self.action == 'list':
            return PublicationListSerializer
        return PublicationDetailSerializer
