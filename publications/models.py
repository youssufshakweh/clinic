from django.db import models
from nutritionists.models import Nutritionist


class EducationalPublication(models.Model):
    STATUS_CHOICES = [
        ('draft', 'مسودة'),
        ('published', 'منشورة'),
        ('archived', 'مؤرشفة'),
    ]
    
    publication_id = models.AutoField(primary_key=True)
    nutritionist = models.ForeignKey(Nutritionist, on_delete=models.CASCADE, related_name='publications', verbose_name='أخصائي التغذية')
    title = models.CharField(max_length=255, verbose_name='العنوان')
    overview = models.TextField(verbose_name='النبذة')
    content = models.TextField(verbose_name='المحتوى')
    last_sentence = models.CharField(max_length=255, blank=True, verbose_name='الجملة الأخيرة')
    img = models.ImageField(upload_to='publications/', blank=True, null=True, verbose_name='الصورة')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='الحالة')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True, verbose_name='تاريخ النشر')
    
    class Meta:
        db_table = 'educational_publication'
        verbose_name = 'منشور تعليمي'
        verbose_name_plural = 'المنشورات التعليمية'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['nutritionist', 'status']),
            models.Index(fields=['published_at']),
        ]
    
    def __str__(self):
        return self.title