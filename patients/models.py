from django.db import models
from users.models import User
from django.core.validators import RegexValidator

# Create your models here.

class Patient(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='patient_profile'
    )
    

    height = models.FloatField(
        verbose_name="الطول"
    )

    start_weight = models.FloatField(
        verbose_name="الوزن عند البدء"
    )

    profile_image = models.ImageField(
        upload_to='patients/',
        blank=True,
        null=True,
        verbose_name='صورة الملف'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patient'
        verbose_name = 'مريض'
        verbose_name_plural = 'المرضى'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Measurement(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="measurements",
        verbose_name="المريض"
    )

    date = models.DateField(verbose_name="تاريخ القياس")

    weight = models.FloatField(verbose_name="الوزن")
    waist = models.FloatField(verbose_name="الخصر")
    abdomen = models.FloatField(verbose_name="البطن")
    hip = models.FloatField(verbose_name="الورك")
    thigh = models.FloatField(verbose_name="الفخذ")
    arm = models.FloatField(verbose_name="الذراع")

    bmi = models.FloatField(verbose_name="مؤشر كتلة الجسم")

    class Meta:
        db_table = 'measurement'
        verbose_name = 'قياس'
        verbose_name_plural = 'القياسات'
        ordering = ['-date']

    def __str__(self):
        return f"قياسات {self.patient} بتاريخ {self.date}"

class PatientInitialInfo(models.Model):
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name="initial_info")

    visit_goal = models.CharField(max_length=255, blank=True)
    followed_diet_before = models.BooleanField(default=False)

    status = models.CharField(
        max_length=50,
        choices=[
            ('child', 'طفل'),
            ('vegetarian', 'نباتي'),
            ('pregnant', 'حامل'),
            ('breastfeeding', 'مرضع'),
        ],
        blank=True
    )

    favorite_color = models.CharField(max_length=100, blank=True)

    surgeries = models.TextField(blank=True)
    last_analysis = models.TextField(blank=True)
    doctor_diagnosis = models.TextField(blank=True)
    visit_purpose = models.TextField(blank=True)
    medications = models.TextField(blank=True)

    # مشاكل صحية
    has_pressure = models.BooleanField(default=False)
    has_diabetes = models.BooleanField(default=False)
    has_cholesterol = models.BooleanField(default=False)
    has_colon = models.BooleanField(default=False)
    has_constipation = models.BooleanField(default=False)
    has_thyroid = models.BooleanField(default=False)
    has_food_allergy = models.BooleanField(default=False)
    has_pcos = models.BooleanField(default=False)
    has_irregular_period = models.BooleanField(default=False)

    # أدوية
    takes_cortisone = models.BooleanField(default=False)
    takes_birth_control = models.BooleanField(default=False)
    takes_allergy_med = models.BooleanField(default=False)
    takes_glucose_regulator = models.BooleanField(default=False)
    takes_cycle_regulator = models.BooleanField(default=False)
    takes_retan = models.BooleanField(default=False)
