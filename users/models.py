from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date
from django.core.validators import RegexValidator

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
        verbose_name='العنوان'
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def age(self):
        today = date.today()
        if self.birth_date: 
            return today.year - self.birth_date.year - ((today.month, today.day) < 
                                                        (self.birth_date.month, self.birth_date.day) )
        return None
    
        
    # تسجيل الدخول عن طريق الايميل
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    