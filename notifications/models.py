from django.db import models
from django.conf import settings
from patients.models import Patient

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)

    sender = models.CharField(max_length=255, verbose_name='مرسل الرسالة')
    email = models.EmailField(verbose_name='البريد الإلكتروني')
    subject = models.CharField(max_length=255, verbose_name='الموضوع')
    message = models.TextField(verbose_name='الرسالة')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإرسال')

    reply = models.TextField(blank=True, null=True, verbose_name='الرد')
    reply_date = models.DateTimeField(blank=True, null=True, verbose_name='تاريخ الرد')

    is_read = models.BooleanField(default=False, verbose_name='مقروءة')

    sender_type = models.CharField(
        max_length=20,
        choices=[('patient', 'مريض'), ('visitor', 'زائر')],
        default='visitor',
        verbose_name='نوع المرسل'
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='المريض (إن وجد)'
    )

    class Meta:
        db_table = 'message'
        verbose_name = 'رسالة'
        verbose_name_plural = 'الرسائل'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_read']),
        ]

    def __str__(self):
        return f"{self.sender} - {self.subject}"
class Notification(models.Model):
    STATUS_CHOICES = [
        ('unread', 'غير مقروءة'),
        ('read', 'مقروءة'),
        ('archived', 'مؤرشفة'),
    ]

    TYPE_CHOICES = [
        ('appointment_reminder', 'تذكير موعد'),
        ('order_update', 'تحديث طلب'),
        ('general', 'عام'),
    ]

    notification_id = models.AutoField(primary_key=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', verbose_name='المستلم', null=True,blank=True)
    title = models.CharField(max_length=255, verbose_name='العنوان')
    info = models.TextField(verbose_name='المعلومات')
    time = models.DateTimeField(auto_now_add=True, verbose_name='الوقت')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unread', verbose_name='الحالة')

    message = models.TextField(blank=True, null=True, verbose_name='الرسالة')
    is_read = models.BooleanField(default=False, verbose_name='مقروء')
    notification_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name='نوع الإشعار'
    )
    created_at = models.DateTimeField(auto_now_add=True,null=True, verbose_name='تاريخ الإنشاء')

    class Meta:
        db_table = 'notification'
        verbose_name = 'إشعار'
        verbose_name_plural = 'الإشعارات'
        ordering = ['-time']
        indexes = [
            models.Index(fields=['recipient', 'status']),
        ]

    def __str__(self):
        return f"{self.recipient} - {self.title}"