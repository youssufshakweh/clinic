from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from patients.models import Patient
from appointments.models import Appointment
from nutritionists.models import Nutritionist, Product
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


class Cart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    patient = models.OneToOneField(
        Patient,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart - {self.patient}"


class CartItem(models.Model):
    cart_item_id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items'
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items',
        verbose_name='الموعد'
    )
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        filled = sum(1 for x in [self.product, self.package, self.appointment] if x)
        if filled > 1:
            raise ValidationError('CartItem must have exactly one of: product, package, or appointment.')
        if filled == 0:
            raise ValidationError('CartItem must have exactly one of: product, package, or appointment.')
        super().save(*args, **kwargs)

    def __str__(self):
        item = self.product or self.package or self.appointment
        return f"{item} x {self.quantity}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'قيد الانتظار'),
        ('confirmed', 'مؤكد'),
        ('cancelled', 'ملغى'),
        ('rejected', 'مرفوض'),
    ]

    order_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.order_id} - {self.patient}"


class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    package = models.ForeignKey(
        Package,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items'
    )
    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='order_items',
        verbose_name='الموعد'
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        item = self.product or self.package or self.appointment
        return f"{item} x {self.quantity} @ {self.price}"


class PaymentTransaction(models.Model):
    id = models.AutoField(primary_key=True)
    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='رقم المعاملة'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_transactions',
        verbose_name='المستخدم'
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payment_transactions',
        verbose_name='الطلب'
    )
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإرسال')

    class Meta:
        db_table = 'payment_transaction'
        verbose_name = 'معاملة دفع'
        verbose_name_plural = 'معاملات الدفع'
        ordering = ['-submitted_at']

    def __str__(self):
        return f"Transaction {self.transaction_id} - Order #{self.order_id}"
