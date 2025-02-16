from django.db import models
from django.contrib.auth.models import User

class Role(models.TextChoices):
    MANAGER = 'MANAGER', 'YÖNETİCİ'
    CUSTOMER = 'CUSTOMER', 'MÜŞTERİ'
    SELLER = 'SELLER', 'SATICI'
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices)
    phone = models.CharField(max_length=30, blank=True, null=True)