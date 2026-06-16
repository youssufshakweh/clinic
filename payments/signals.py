from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Payment
from notifications.models import Notification
PAYMENT_TYPE_AR = {
    'appointment': 'موعد',
    'product': 'منتج',
    'package': 'باقة',
    'workshop': 'ورشة عمل',
}

PAYMENT_STATUS_AR = {
    'pending': 'قيد الانتظار',
    'completed': 'مكتمل',
    'failed': 'فشل',
    'refunded': 'مرجع',
}


@receiver(post_save, sender=Payment)
def create_payment_notification(sender, instance, created, **kwargs):
    patient_user = instance.user 
    payment_type = PAYMENT_TYPE_AR.get(instance.type, instance.type)
    payment_status = PAYMENT_STATUS_AR.get(instance.status, instance.status)
    payment_date = instance.date.strftime("%Y/%m/%d")
    amount = f"{instance.amount} s.p" 
    
    # ===== عند إنشاء الدفع لأول مرة =====
    if created:
        Notification.objects.create(
            recipient=patient_user,
            title="تم استلام طلب الدفع",
            info=(
                f"تم استلام طلب دفعك بمبلغ {amount} "
                f"مقابل {payment_type} بتاريخ {payment_date}."
            ),
            message=(
                f"مرحباً،\n"
                f"تم استلام طلب الدفع الخاص بك بنجاح.\n\n"
                f"💳 النوع: {payment_type}\n"
                f"💰 المبلغ: {amount}\n"
                f"📅 التاريخ: {payment_date}\n"
                f"📋 الحالة: {payment_status}\n"
                f"🔖 رقم المعاملة: {instance.transaction_id or 'غير متوفر'}\n\n"
                f"سيتم إشعارك عند تأكيد الدفع."
            ),
            status="unread",
            is_read=False,
        )
        return

    # ===== عند تحديث حالة الدفع =====
    if instance.status == 'completed':
        Notification.objects.create(
            recipient=patient_user,
            title="✅ تم تأكيد الدفع",
            info=(
                f"تم تأكيد دفعك بمبلغ {amount} مقابل {payment_type} بنجاح."
            ),
            message=(
                f"مرحباً،\n"
                f"يسعدنا إعلامك بأن عملية الدفع تمت بنجاح.\n\n"
                f"💳 النوع: {payment_type}\n"
                f"💰 المبلغ: {amount}\n"
                f"📅 التاريخ: {payment_date}\n"
                f"🔖 رقم المعاملة: {instance.transaction_id or 'غير متوفر'}\n\n"
                f"شكراً لك!"
            ),
            status="unread",
            is_read=False,
        )

    elif instance.status == 'failed':
        Notification.objects.create(
            recipient=patient_user,
            title="❌ فشلت عملية الدفع",
            info=(
                f"فشلت عملية دفعك بمبلغ {amount} مقابل {payment_type}."
            ),
            message=(
                f"مرحباً،\n"
                f"نأسف لإعلامك بأن عملية الدفع قد فشلت.\n\n"
                f"💳 النوع: {payment_type}\n"
                f"💰 المبلغ: {amount}\n"
                f"📅 التاريخ: {payment_date}\n"
                f"🔖 رقم المعاملة: {instance.transaction_id or 'غير متوفر'}\n\n"
                f"يُرجى المحاولة مرة أخرى أو التواصل مع الدعم."
            ),
            status="unread",
            is_read=False,
        )

    elif instance.status == 'refunded':
        Notification.objects.create(
            recipient=patient_user,
            title="🔄 تم استرجاع المبلغ",
            info=(
                f"تم استرجاع مبلغ {amount} الخاص بـ {payment_type} بنجاح."
            ),
            message=(
                f"مرحباً،\n"
                f"تم معالجة طلب الاسترجاع الخاص بك بنجاح.\n\n"
                f"💳 النوع: {payment_type}\n"
                f"💰 المبلغ المسترجع: {amount}\n"
                f"📅 التاريخ: {payment_date}\n"
                f"🔖 رقم المعاملة: {instance.transaction_id or 'غير متوفر'}\n\n"
                f"سيتم إعادة المبلغ خلال 3-5 أيام عمل."
            ),
            status="unread",
            is_read=False,
        )