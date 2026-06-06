from rest_framework import serializers
from .models import EducationalPublication


class PublicationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalPublication
        fields = ['publication_id', 'title', 'img']


class PublicationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationalPublication
        fields = '__all__'
