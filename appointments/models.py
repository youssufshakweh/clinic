from django.db import models

from django.db import models
from patients.models import Patient
from nutritionists.models import Nutritionist




class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('confirmed', 'مؤكد'),
        ('completed', 'اكتمل'),
        ('cancelled', 'ملغى'),
        ('no-show', 'لم يحضر'),
    ]
    
    TYPE_CHOICES = [
        ('online', 'أونلاين'),
        ('in-person', 'حضوري'),
    ]
    
    app_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='المريض'
    )
    nutritionist = models.ForeignKey(
        Nutritionist,
        on_delete=models.CASCADE,
        related_name='appointments',
        verbose_name='أخصائي التغذية'
    )
    date = models.DateField(verbose_name='التاريخ')
    time = models.TimeField(verbose_name='الوقت')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='الحالة'
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name='نوع الموعد'
    )
    start_time = models.TimeField(null=True, blank=True, verbose_name='وقت البداية')
    end_time = models.TimeField(null=True, blank=True, verbose_name='وقت الانتهاء')
    notes = models.TextField(blank=True, verbose_name='الملاحظات')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointment'
        verbose_name = 'موعد'
        verbose_name_plural = 'المواعيد'
        ordering = ['-date', '-time']
        unique_together = (('date', 'start_time'),)
        indexes = [
            models.Index(fields=['patient', 'date']),
            models.Index(fields=['nutritionist', 'status']),
        ]
    
    def __str__(self):
        return f"{self.patient} - {self.date} {self.time}"

class Schedule(models.Model):
    DAY_CHOICES = [
        ('monday', 'الإثنين'),
        ('tuesday', 'الثلاثاء'),
        ('wednesday', 'الأربعاء'),
        ('thursday', 'الخميس'),
        ('friday', 'الجمعة'),
        ('saturday', 'السبت'),
        ('sunday', 'الأحد'),
    ]

    day_of_week = models.CharField(
        max_length=20,
        choices=DAY_CHOICES,
        unique=True,
        verbose_name='اليوم'
    )
    start_time = models.TimeField(verbose_name='وقت بداية الدوام')
    end_time = models.TimeField(verbose_name='وقت انتهاء الدوام')

    class Meta:
        db_table = 'schedule'
        verbose_name = 'جدول'
        verbose_name_plural = 'الجداول'
        ordering = ['day_of_week']

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.start_time} - {self.end_time}"