from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


@shared_task
def send_appointment_reminders():
    from appointments.models import Appointment
    from .models import Notification

    tomorrow = timezone.now().date() + timezone.timedelta(days=1)

    appointments = Appointment.objects.filter(
        date=tomorrow,
        status='confirmed',
    ).select_related('patient__user')

    count = 0
    for appointment in appointments:
        recipient = appointment.patient.user
        slot_time = appointment.start_time or appointment.time
        title = 'تذكير بموعدك غداً'
        message = f'لديك موعد غداً بتاريخ {appointment.date} في الساعة {slot_time}'

        Notification.objects.create(
            recipient=recipient,
            title=title,
            info=message,
            message=message,
            is_read=False,
            notification_type='appointment_reminder',
        )

        try:
            send_mail(
                subject=title,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient.email],
                fail_silently=True,
            )
        except Exception:
            pass

        count += 1

    return f'Sent reminders for {count} appointments'


@shared_task
def send_order_status_update(order_id):
    from payments.models import Order
    from .models import Notification

    try:
        order = Order.objects.select_related('patient__user').get(order_id=order_id)
    except Order.DoesNotExist:
        return f'Order {order_id} not found'

    recipient = order.patient.user
    title = f'تحديث حالة طلبك #{order.order_id}'
    message = f'تم تحديث حالة طلبك إلى: {order.get_status_display()}'

    Notification.objects.create(
        recipient=recipient,
        title=title,
        info=message,
        message=message,
        is_read=False,
        notification_type='order_update',
    )

    try:
        send_mail(
            subject=title,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient.email],
            fail_silently=True,
        )
    except Exception:
        pass

    return f'Sent order update notification for order #{order_id}'
