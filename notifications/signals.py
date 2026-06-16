from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from django.core.mail import send_mail

from contact.models import Inquiry
from nutritionists.models import Product, Nutritionist
from appointments.models import Appointment
from payments.models import Payment


@receiver(post_save, sender=Inquiry)
def notify_new_inquiry(sender, instance, created, **kwargs): 
    if not created: 
        return
    

    from django.contrib.auth import get_user_model

    User = get_user_model()

    # اذا كانت الرسالة من حساب مسجل
    try: 
        user = User.objects.get(email=instance.email)
        patient = user.patient_profile

        Notification.objects.create(
                title="رسالة جديدة من " + user.full_name,
                info=f"أرسل {instance.name} استفساراً جديداً\nالهاتف: {instance.phone}\nالرسالة: {instance.message}",
                patient = patient
        )
    # اذا كانت ارسالة من زائر
    except User.DoesNotExist: 
        send_mail(
        subject=f"استفسار جديد من {instance.name}",
        message=f"الاسم: {instance.name}\nالإيميل: {instance.email}\nالهاتف: {instance.phone}\n\nالرسالة:\n{instance.message}",
        from_email=None,
        recipient_list=[""],
        fail_silently=True,
    )
    except AttributeError: 
        pass

LOW_STOCK_THRESHOLD = 5 

@receiver(post_save, sender=Product)
def notify_low_stock(sender, instance, **kwargs):
    if instance.stock <= LOW_STOCK_THRESHOLD:
        nutritionist = Nutritionist.objects.first()  # بما إنه في أخصائي واحد بالنظام
        if not nutritionist:
            return
        
        # تحقق إنه ما في إشعار غير مقروء لنفس المنتج
        already_notified = Notification.objects.filter(
            nutritionist=nutritionist,
            title=f'تنبيه: مخزون منخفض - {instance.name}',
            status='unread'
        ).exists()
        
        if not already_notified:
            Notification.objects.create(
                nutritionist=nutritionist,
                title=f'تنبيه: مخزون منخفض - {instance.name}',
                info=f'الكمية المتبقية من {instance.name} وصلت إلى {instance.stock} وحدات فقط.',
            )

APPOINTMENT_TYPE_AR = {
    'online': 'أونلاين',
    'in-person': 'حضوري',
}

@receiver(post_save, sender=Appointment)
def create_appointment_notification(sender, instance, created, **kwargs):
    if not created:
        return

    appointment_date = instance.date.strftime("%Y/%m/%d")
    appointment_time = instance.time.strftime("%I:%M %p")
    appointment_type = APPOINTMENT_TYPE_AR.get(instance.type, instance.type)
    nutritionist_name = instance.nutritionist.user.get_full_name()  # adjust if needed

    # Notify the patient
    Notification.objects.create(
        recipient=instance.patient.user,  # adjust if Patient has a different user field
        title="تأكيد حجز موعدك",
        info=(
            f"تم حجز موعدك مع أخصائي التغذية {nutritionist_name} "
            f"بتاريخ {appointment_date} الساعة {appointment_time} ({appointment_type})."
        ),
        message=(
            f"مرحباً،\n"
            f"نود إعلامك بأنه تم حجز موعدك بنجاح.\n\n"
            f"👨‍⚕️ أخصائي التغذية: {nutritionist_name}\n"
            f"📅 التاريخ: {appointment_date}\n"
            f"⏰ الوقت: {appointment_time}\n"
            f"🏥 نوع الموعد: {appointment_type}\n\n"
            f"يُرجى الحضور قبل 10 دقائق من الموعد المحدد."
        ),
        status="unread",
        is_read=False,
    )

    # Notify the nutritionist
    patient_name = instance.patient.user.get_full_name()  # adjust if needed

    Notification.objects.create(
        recipient=instance.nutritionist.user,  # adjust if Nutritionist has a different user field
        title="موعد جديد",
        info=(
            f"تم حجز موعد جديد مع المريض {patient_name} "
            f"بتاريخ {appointment_date} الساعة {appointment_time} ({appointment_type})."
        ),
        message=(
            f"لديك موعد جديد تم حجزه.\n\n"
            f"👤 المريض: {patient_name}\n"
            f"📅 التاريخ: {appointment_date}\n"
            f"⏰ الوقت: {appointment_time}\n"
            f"🏥 نوع الموعد: {appointment_type}\n"
        ),
        status="unread",
        is_read=False,
    )