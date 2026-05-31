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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'appointment'
        verbose_name = 'موعد'
        verbose_name_plural = 'المواعيد'
        ordering = ['-date', '-time']
        unique_together = ('patient', 'nutritionist', 'date', 'time')
        indexes = [
            models.Index(fields=['patient', 'date']),
            models.Index(fields=['nutritionist', 'status']),
        ]
    
    def __str__(self):
        return f"{self.patient} - {self.date} {self.time}"

class Note (models.Model):
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE 
    )
    name = models.CharField(max_length=100, blank=True) 
    content = models.CharField(max_length=1000, blank=True) 