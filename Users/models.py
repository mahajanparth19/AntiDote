from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)

    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="Patient")
    Name = models.CharField(max_length=80,default = None,null=True)
    Age = models.IntegerField(default = None,null=True)
    Address = models.TextField(max_length=300,null=True)
    Gender = models.CharField(max_length=30,null=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="Doctor")
    Name = models.CharField(max_length=80,default = None,null=True)
    Age = models.IntegerField(default = None,null=True)
    Address = models.TextField(max_length=300,null=True)
    Gender = models.CharField(max_length=30,null=True)
    Specialization = models.CharField(max_length=80,null=True)
    contact  = models.IntegerField(null=True)
    Qualification = models.CharField(max_length=30,null=True)