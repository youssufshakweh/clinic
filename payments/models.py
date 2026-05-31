from django.db import models
from patients.models import Patient
from appointments.models import Appointment
from nutritionists.models import Nutritionist
from subscriptions.models import Package


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
        ('refunded', 'مرجع'),
    ]
    
    TYPE_CHOICES = [
        ('appointment', 'موعد'),
        ('product', 'منتج'),
        ('package', 'باقة'),
        ('workshop', 'ورشة عمل'),
    ]
    
    payment_id = models.AutoField(primary_key=True)

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='المريض'
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='الموعد'
    )

    nutritionist = models.ForeignKey(
        Nutritionist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='أخصائي التغذية'
    )

    # from django.db import models


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('completed', 'مكتمل'),
        ('failed', 'فشل'),
        ('refunded', 'مرجع'),
    ]
    
    TYPE_CHOICES = [
        ('appointment', 'موعد'),
        ('product', 'منتج'),
        ('package', 'باقة'),
        ('workshop', 'ورشة عمل'),
    ]
    
    payment_id = models.AutoField(primary_key=True)

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='المريض'
    )

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='الموعد'
    )

    nutritionist = models.ForeignKey(
        Nutritionist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='أخصائي التغذية'
    )
# لأنو ممكن تكون دفعة لمنتج أو موعد، مو شرط باقة --> on_delete=models.SET_NULL,

    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='الباقة'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المبلغ')
    date = models.DateField(verbose_name='التاريخ')
    time = models.TimeField(verbose_name='الوقت')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='الحالة'
    )

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        verbose_name='النوع'
    )

    payment_method = models.CharField(max_length=50, blank=True, verbose_name='طريقة الدفع')

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        unique=True,
        verbose_name='معرف المعاملة'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment'
        verbose_name = 'دفعة'
        verbose_name_plural = 'الدفعات'
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        return f"{self.patient} - {self.amount} - {self.status}"

    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='الباقة'
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='المبلغ')
    date = models.DateField(verbose_name='التاريخ')
    time = models.TimeField(verbose_name='الوقت')

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='الحالة'
    )

    type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES,
        verbose_name='النوع'
    )

    payment_method = models.CharField(max_length=50, blank=True, verbose_name='طريقة الدفع')

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        unique=True,
        verbose_name='معرف المعاملة'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment'
        verbose_name = 'دفعة'
        verbose_name_plural = 'الدفعات'
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['transaction_id']),
        ]
    
    def __str__(self):
        return f"{self.patient} - {self.amount} - {self.status}"
