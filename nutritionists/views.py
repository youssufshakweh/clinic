from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q

from .models import Product
from .serializers import ProductSerializer
from .permissions import IsNutritionistOwnerOrReadOnly

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsNutritionistOwnerOrReadOnly]  # ← هون التغيير
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    def perform_create(self, serializer):
        nutritionist = self.request.user.nutritionist_profile
        serializer.save(nutritionist=nutritionist)

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-created_at')

        product_type = self.request.query_params.get("type")
        if product_type:
            queryset = queryset.filter(type=product_type)

        search = self.request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(type__icontains=search)
            )

        return queryset

    @action(detail=True, methods=['post'])
    def increase_quantity(self, request, pk=None):
        product = self.get_object()  # has_object_permission بتشتغل هون تلقائياً
        product.quantity += 1
        product.save()
        return Response({"quantity": product.quantity})

    @action(detail=True, methods=['post'])
    def decrease_quantity(self, request, pk=None):
        product = self.get_object()
        if product.quantity > 0:
            product.quantity -= 1
            product.save()
        return Response({"quantity": product.quantity})

    @action(detail=True, methods=['post'])
    def upload_image(self, request, pk=None):
        product = self.get_object()
        img = request.FILES.get("img")

        if not img:
            return Response({"error": "لم يتم إرسال صورة"}, status=status.HTTP_400_BAD_REQUEST)

        product.img = img
        product.save()

        return Response({
            "message": "تم رفع الصورة بنجاح",
            "img_url": request.build_absolute_uri(product.img.url)
        })

    @action(detail=True, methods=['post'])
    def toggle_available(self, request, pk=None):
        product = self.get_object()
        product.is_available = not product.is_available
        product.save()

        return Response({
            "product_id": product.product_id,
            "is_available": product.is_available
        })