from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .managers import CustomUserManager


class Patient(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    Name = models.CharField(max_length=80,default = None,null=True)
    Age = models.IntegerField(default = None,null=True)
    Address = models.TextField(max_length=300,null=True)
    Gender = models.CharField(max_length=30,null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email