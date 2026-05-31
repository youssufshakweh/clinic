from django.db import models
from users.models import User
from django.core.validators import RegexValidator
from clinic.models import Clinic

class Nutritionist(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='nutritionist_profile',
        verbose_name='حساب المستخدم'
    )

    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name='nutritionists',
        verbose_name='العيادة'
    )
    phone_validator = RegexValidator(
    regex=r'^\+?[1-9]\d{7,14}$',
    message="الرجاء إدخال رقم هاتف دولي صالح")



    phone = models.CharField(
    max_length=20,
    validators=[phone_validator],
    verbose_name="رقم الهاتف"
)

    specialization = models.CharField(max_length=255, verbose_name='التخصص')
    overview = models.TextField(blank=True, verbose_name='نبذة')

    profile_image = models.ImageField(
        upload_to='nutritionists/',
        blank=True,
        null=True,
        verbose_name='صورة الملف'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'nutritionist'
        verbose_name = 'أخصائي تغذية'
        verbose_name_plural = 'أخصائيو التغذية'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['clinic']),
        ]

    def __str__(self):
        return self.user.get_full_name() or self.user.username


class Product(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ('herbal', 'عشبية صحية'),
        ('tools', 'أدوات الصحة'),
        ('snacks', 'سناكات صحية'),
    ]
    
    product_id = models.AutoField(primary_key=True)

    nutritionist = models.ForeignKey(
        Nutritionist,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='أخصائي التغذية'
    )

    name = models.CharField(max_length=255, verbose_name='اسم المنتج')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='السعر')
    quantity = models.IntegerField(verbose_name='الكمية')

    img = models.ImageField(upload_to='products/', verbose_name='الصورة')

    type = models.CharField(
        max_length=50,
        choices=PRODUCT_TYPE_CHOICES,
        verbose_name='النوع'
    )

    description = models.TextField(blank=True, verbose_name='الوصف')

    is_available = models.BooleanField(default=True, verbose_name='متاح')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'product'
        verbose_name = 'منتج'
        verbose_name_plural = 'المنتجات'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['nutritionist']),
            models.Index(fields=['is_available']),
        ]
    
    def __str__(self):
        return self.name
    

class Availability(models.Model):
    DAYS_CHOICES = [
        ('saturday', 'السبت'),
        ('sunday', 'الأحد'),
        ('monday', 'الإثنين'),
        ('tuesday', 'الثلاثاء'),
        ('wednesday', 'الأربعاء'),
        ('thursday', 'الخميس'),
        ('friday', 'الجمعة'),
    ]
    
    availability_id = models.AutoField(primary_key=True)

    clinic = models.ForeignKey(
        Clinic,
        on_delete=models.CASCADE,
        related_name='availabilities',
        verbose_name='العيادة'
    )

    nutritionist = models.ForeignKey(
        Nutritionist,
        on_delete=models.CASCADE,
        related_name='availabilities',
        verbose_name='أخصائي التغذية'
    )

    day = models.CharField(max_length=20, choices=DAYS_CHOICES, verbose_name='اليوم')
    is_open = models.BooleanField(default=False, verbose_name='مفتوح')
    start_time = models.TimeField(verbose_name='وقت البداية', null=True, blank=True)
    end_time = models.TimeField(verbose_name='وقت الإغلاق')
    online_start_time = models.TimeField(null=True, blank=True, verbose_name='بداية الخدمة الأونلاين')
    online_end_time = models.TimeField(null=True, blank=True, verbose_name='نهاية الخدمة الأونلاين')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'availability'
        verbose_name = 'التوفرية'
        verbose_name_plural = 'التوفريات'
        unique_together = ('clinic', 'nutritionist', 'day')   # ← تصحيح
        indexes = [
            models.Index(fields=['clinic', 'nutritionist']),  # ← تصحيح
            models.Index(fields=['day']),
        ]
    
    def __str__(self):
        return f"{self.nutritionist} - {self.day}"   # ← تصحيح
