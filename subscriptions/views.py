from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from utils.permissions import IsPatientUser
from django.db.models import Count

from .models import Package, Workshop, PatientWorkshop
from .serializers import PackageSerializer, WorkshopListSerializer
from utils.pagination import StandardPagination
from .permissions import IsNutritionistOwnerOrReadOnly


class PackageViewSet(ModelViewSet):
    queryset = Package.objects.all().order_by('-created_at')
    serializer_class = PackageSerializer
    permission_classes = [IsNutritionistOwnerOrReadOnly]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 10
    
    def perform_create(self, serializer):
        nutritionist = self.request.user.nutritionist_profile
        serializer.save(nutritionist=nutritionist)
    @action(detail=False, methods=['get'])
    def stats(self, request):
        # احصاء عدد الاشتراكات لكل باقة
        stats = Package.objects.annotate(
            subscribers_count=Count('payments')
        ).values('package_id', 'name', 'subscribers_count')

        # إجمالي الاشتراكات
        total = sum(item['subscribers_count'] for item in stats)

        # تجهيز النسب المئوية
        for item in stats:
            item['percentage'] = (
                round((item['subscribers_count'] / total) * 100, 2)
                if total > 0 else 0
            )

        # الباقة الأكثر مبيعًا
        most_sold = max(stats, key=lambda x: x['subscribers_count']) if stats else None

        # الباقة الأقل مبيعًا
        least_sold = min(stats, key=lambda x: x['subscribers_count']) if stats else None

        # بيانات الرسم البياني
        chart_data = [
            {
                "label": item['name'],
                "value": item['subscribers_count'],
                "percentage": item['percentage']
            }
            for item in stats
        ]

        return Response({
            "total_subscribers": total,
            "packages": stats,
            "most_sold": most_sold,
            "least_sold": least_sold,
            "chart_data": chart_data,
        })


class WorkshopViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = WorkshopListSerializer
    pagination_class = StandardPagination

    def get_queryset(self):
        return Workshop.objects.filter(
            status__in=['upcoming', 'ongoing']
        ).order_by('date', 'time')

    def get_permissions(self):
        if self.action == 'register':
            return [IsPatientUser()]
        return [AllowAny()]

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        workshop = self.get_object()

        if not hasattr(request.user, 'patient_profile'):
            return Response(
                {'error': 'Only patients can register for workshops'},
                status=status.HTTP_403_FORBIDDEN
            )

        patient = request.user.patient_profile

        if PatientWorkshop.objects.filter(patient=patient, workshop=workshop).exists():
            return Response(
                {'error': 'Already registered for this workshop'},
                status=status.HTTP_400_BAD_REQUEST
            )

        PatientWorkshop.objects.create(patient=patient, workshop=workshop)
        return Response(
            {'message': 'Successfully registered for the workshop'},
            status=status.HTTP_201_CREATED
        )