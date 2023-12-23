from django.db import models
from django.utils.timezone import now

# Create your models here.

class Unit(models.Model):
    uom = models.CharField(max_length=64, null=True, blank=True, unique=True)  # uom = unit of measurement
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)  
    
    def __str__(self):
        return self.uom