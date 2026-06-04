from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date, timedelta
from django.core.validators import RegexValidator
import random

class User(AbstractUser):
    
    class Gender (models.TextChoices):
        Male = 'male' , 'Male'
        Female = 'female' , 'Female'
    class Status (models.TextChoices):
        Active = 'active' , 'Active'
        Deactive = 'deactive' , 'Deactive'
    
    phone_validator = RegexValidator(
        regex=r'^\+?[1-9]\d{7,14}$',
        message="الرجاء إدخال رقم هاتف دولي صالح"
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15 , blank=True , null=True)
    birth_date = models.DateField(blank=True , null=True)

    gender = models.CharField(max_length=100 , choices=  Gender.choices , null= True , blank=True)
    status = models.CharField(max_length=100 , choices= Status.choices , default=Status.Active)
    

    address = models.CharField(
        max_length=255,
        verbose_name='العنوان',
        blank=True,
        null=True
    )

    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_created_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        today = date.today()
        if self.birth_date: 
            return today.year - self.birth_date.year - ((today.month, today.day) < 
                                                        (self.birth_date.month, self.birth_date.day) )
        return None
    
    def generate_otp(self):
        """توليد رمز OTP عشوائي"""
        self.otp = str(random.randint(100000, 999999))
        self.otp_created_at = timezone.now()
        self.save()
        return self.otp
    
    def verify_otp(self, otp_code):
        """التحقق من صحة الرمز والوقت"""
        if self.otp != otp_code:
            return False
        
        # تحقق من انتهاء صلاحية الرمز (10 دقائق)
        if timezone.now() - self.otp_created_at > timedelta(minutes=10):
            return False
        
        return True
        
    # تسجيل الدخول عن طريق الايميل
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    