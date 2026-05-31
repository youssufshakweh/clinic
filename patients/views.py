from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Patient
from .serializers import PatientSerializer , PatientDetailSerializer

class PatientViewSet(ModelViewSet):
    queryset = Patient.objects.all().order_by('-created_at')
    serializer_class = PatientSerializer   # لعرض المرضى
    # عرض ملف المريض الكامل
    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        patient = self.get_object()
        serializer = PatientDetailSerializer(patient)
        return Response(serializer.data)