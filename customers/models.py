from datetime import datetime, timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from customers.managers import CustomUserManager


# Create your models here.
class Customer(models.Model):
    full_name = models.CharField(max_length=155, null=True, blank=True)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    joined = models.DateTimeField(default=datetime.now())
    image = models.ImageField(upload_to='customer/', null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = 'All Customers'


class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(unique=True, max_length=13)
    username = models.CharField(max_length=35, null=True, blank=True)
    birth_of_date = models.DateField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone
