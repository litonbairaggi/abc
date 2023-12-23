from django.db import models
from django.utils.timezone import now
from datetime import date
# Create your models here.


class Myapp(models.Model):
    name = models.CharField(max_length=64, null=True, unique=True, blank=True)

    def __str__(self):
        return self.name