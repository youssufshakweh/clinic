from django.db import models
from django.core.validators import RegexValidator


class Clinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name='اسم العيادة')
    email = models.EmailField(verbose_name='البريد الإلكتروني',unique=True)
    phone_validator = RegexValidator(
    regex=r'^\+?[1-9]\d{7,14}$',
    message="الرجاء إدخال رقم هاتف دولي صالح"
)

    phone = models.CharField(
    max_length=20,
    validators=[phone_validator],
    verbose_name="رقم الهاتف"
)
    logo = models.ImageField(upload_to='clinic/', blank=True, null=True, verbose_name='الشعار')
    address = models.CharField(max_length=255, verbose_name='العنوان', blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='خط العرض')
    longitude = models.DecimalField(max_digits=9, decimal_places=7, verbose_name='خط الطول')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clinic'
        verbose_name = 'عيادة'
        verbose_name_plural = 'العيادات'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return self.name
