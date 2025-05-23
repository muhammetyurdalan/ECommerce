import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class City(models.Model):
    name = models.CharField(max_length=50)


class Role(models.TextChoices):
    MANAGER = 'MANAGER', 'YÖNETİCİ'
    CUSTOMER = 'CUSTOMER', 'MÜŞTERİ'
    SELLER = 'SELLER', 'SATICI'
    ADMIN = 'ADMIN', 'ADMİN'


class Language(models.TextChoices):
    tr = 'tr'
    en = 'en'
    

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        user = self.model(username=username, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('role', Role.ADMIN)
        return self.create_user(username, password, **kwargs)
    
class User(AbstractBaseUser):
    uuid = models.UUIDField(default=uuid.uuid4)
    role = models.CharField(max_length=20, choices=Role.choices)
    username = models.CharField(max_length=20, unique=True)
    email = models.CharField(max_length=100)
    language = models.CharField(max_length=2, choices=Language.choices, default='tr')
    phone = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    status = models.SmallIntegerField(
        choices=[(1, 'ACTIVE'), (2, 'PASSIVE'), (3, 'SUSPEND')], default=1)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    iban = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=255, blank=True)
    id_number = models.CharField(max_length=11, blank=True)
    city = models.ForeignKey(City, related_name="users", on_delete=models.SET_NULL, 
        blank=True, null=True)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'password']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.email