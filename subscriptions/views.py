from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count

from .models import Package
from .serializers import PackageSerializer


class PackageViewSet(ModelViewSet):
    queryset = Package.objects.all().order_by('-created_at')
    serializer_class = PackageSerializer

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