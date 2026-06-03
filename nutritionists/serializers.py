from rest_framework import serializers
from .models import Availability, Nutritionist, Product

class AvailabilitySerializer(serializers.ModelSerializer):
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)
    nutrionist_name = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Availability
        fields = [
            'availability_id', 'clinic', 'clinic_name', 'nutrionist',
            'nutrionist_name', 'day', 'is_open', 'start_time', 'end_time',
            'online_start_time', 'online_end_time', 'created_at', 'updated_at'
        ]
        read_only_fields = ['availability_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'clinic': {'required': True},
            'nutrionist': {'required': True},
            'day': {'required': True},
            'start_time': {'required': True},
            'end_time': {'required': True},
        }
    
    def get_nutrionist_name(self, obj):
        return f"{obj.nutrionist.first_name} {obj.nutrionist.last_name}"
    

class NutritionistSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)

    clinic_name = serializers.CharField(source='clinic.name', read_only=True)

    class Meta:
        model = Nutritionist
        fields = [
            'nutritionist_id',
            'username',
            'email',
            'clinic',
            'clinic_name',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['nutritionist_id', 'created_at', 'updated_at']
    


class ProductSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'product_id',
            'nutritionist',
            'name',
            'price',
            'quantity',
            'img',
            'img_url',
            'type',
            'description',
            'is_available',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['nutritionist', 'created_at', 'updated_at']

    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.img and request:
            return request.build_absolute_uri(obj.img.url)
        return None
 