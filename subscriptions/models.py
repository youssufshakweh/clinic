from django.db import models
from nutritionists.models import Nutritionist
from patients.models import Patient
class Package(models.Model):
    CATEGORY_CHOICES = [
        ('medical', 'إجراءات علاجية'),
        ('diet', 'حميات صحية'),
    ]

    package_id = models.AutoField(primary_key=True)

    nutritionist = models.ForeignKey(
        Nutritionist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='packages',
        verbose_name='أخصائي التغذية',

    )

    name = models.CharField(max_length=255, verbose_name='اسم الباقة')
    details = models.TextField(verbose_name='مميزات الباقة')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='سعر الباقة')

    num = models.IntegerField(verbose_name='مدة الباقة (بالشهور)')

    first_payment_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='نسبة الدفعة الأولى'
    )

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name='نوع الباقة'
    )

    require_consultation = models.BooleanField(
        default=False,
        verbose_name='استشارة مسبقة'
    )

    status = models.BooleanField(default=True, verbose_name='نشطة')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'package'
        verbose_name = 'باقة'
        verbose_name_plural = 'الباقات'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    


class Workshop(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'قادمة'),  
        ('ongoing', 'جارية'),
        ('completed', 'اكتملت'),
        ('cancelled', 'ملغاة'),
    ]
    
    TYPE_CHOICES = [
        ('online', 'أونلاين'),
        ('in-person', 'حضوري'),
    ]
    
    workshop_id = models.AutoField(primary_key=True)

    # ← تصحيح اسم الحقل والكلاس
    nutritionist = models.ForeignKey(
        Nutritionist,
        on_delete=models.CASCADE,
        related_name='workshops',
        verbose_name='أخصائي التغذية'
    )

    title = models.CharField(max_length=255, verbose_name='العنوان')
    date = models.DateField(verbose_name='التاريخ')
    time = models.TimeField(verbose_name='الوقت')
    place = models.CharField(max_length=255, blank=True, verbose_name='المكان')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='النوع')
    overview = models.TextField(verbose_name='النبذة')
    img = models.ImageField(upload_to='workshops/', blank=True, null=True, verbose_name='الصورة')
    link = models.URLField(blank=True, null=True, verbose_name='الرابط')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming', verbose_name='الحالة')
    num_participants = models.IntegerField(default=0, verbose_name='عدد المشاركين')
    max_participants = models.IntegerField(null=True, blank=True, verbose_name='الحد الأقصى للمشاركين')
    max_attendees = models.PositiveIntegerField(null=True, blank=True, verbose_name='الحد الأقصى للحضور')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'workshop'
        verbose_name = 'ورشة عمل'
        verbose_name_plural = 'ورش العمل'
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['nutritionist', 'date']),  # ← تصحيح هنا أيضًا
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return self.title

    @property
    def is_full(self):
        if self.max_attendees is None:
            return False
        confirmed_count = self.attendances.filter(status='confirmed').count()
        return confirmed_count >= self.max_attendees


class WorkshopAttendance(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('accepted', 'مقبول'),
        ('rejected', 'مرفوض'),
    ]

    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name='attendances',
        verbose_name='الورشة'
    )
    email = models.EmailField(verbose_name='البريد الالكتروني')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التسجيل')
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='الحالة'
    )

    class Meta:
        db_table = 'workshop_attendance'
        verbose_name = 'حضور ورشة'
        verbose_name_plural = 'حضور الورش'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.email} - {self.workshop.title} ({self.status})"


class PatientWorkshop(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='workshop_registrations'
    )
    workshop = models.ForeignKey(
        Workshop,
        on_delete=models.CASCADE,
        related_name='participants'
    )

    class Meta:
        db_table = 'patient_workshop'
        unique_together = ('patient', 'workshop')
        verbose_name = 'اشتراك ورشة'
        verbose_name_plural = 'اشتراكات الورش'
        ordering = ['patient']
    
    def __str__(self):
        return f"{self.patient} - {self.workshop}"

class Plan(models.Model):
    plan_id = models.AutoField(primary_key=True)

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='plans',
        verbose_name='المريض'
    )

    nutritionist = models.ForeignKey(
        Nutritionist,
        on_delete=models.CASCADE,
        related_name='plans',
        verbose_name='أخصائي التغذية'
    )

    file = models.FileField(upload_to='plans/', verbose_name='الملف')

    upload_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الرفع')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخر تحديث')

    description = models.TextField(blank=True, verbose_name='الوصف')
    
    class Meta:
        db_table = 'plan'
        verbose_name = 'خطة غذائية'
        verbose_name_plural = 'الخطط الغذائية'
        ordering = ['-upload_at']
        indexes = [
            models.Index(fields=['patient', 'nutritionist']),
        ]
    
    def __str__(self):
        return f"{self.patient} - Plan"