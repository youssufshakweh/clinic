from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from utils.permissions import IsPatientUser
from utils.pagination import StandardPagination
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(APIView):
    permission_classes = [IsPatientUser]

    def get(self, request):
        recipient = request.user
        notifications = Notification.objects.filter(
            recipient=recipient,
            is_read=False,
        ).order_by('-time')

        paginator = StandardPagination()
        page = paginator.paginate_queryset(notifications, request)
        serializer = NotificationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MarkNotificationReadView(APIView):
    permission_classes = [IsPatientUser]

    def patch(self, request, notification_id):
        try:
            notification = Notification.objects.get(
                notification_id=notification_id,
                recipient=request.user,
            )
        except Notification.DoesNotExist:
            return Response(
                {'error': 'Notification not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        notification.is_read = True
        notification.status = 'read'
        notification.save()

        return Response(NotificationSerializer(notification).data, status=status.HTTP_200_OK)
