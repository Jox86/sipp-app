from django.db import models
from django.conf import settings


class Catalog(models.Model):
    DATA_TYPE_CHOICES = [
        ('products', 'Productos'),
        ('services', 'Servicios'),
        ('both', 'Ambos'),
    ]

    supplier = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    businessType = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    dataType = models.CharField(max_length=20, choices=DATA_TYPE_CHOICES, default='both')
    data = models.JSONField(default=list)
    contractActive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Catálogo'
        verbose_name_plural = 'Catálogos'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.company} - {self.supplier}'