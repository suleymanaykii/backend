# models.py
import uuid
from django.utils import timezone
from django.db import models
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser


class Unit(models.Model):
    name = models.CharField(max_length=100)
    upper_unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='sub_units', null=True)
    sub_unit = models.ForeignKey('Unit', on_delete=models.CASCADE, related_name='upper_units', null=True)

    def clean(self):
        if self.upper_unit and self.upper_unit.upper_unit == self:
            raise ValidationError('Birimin üst birimi kendi alt birimi olamaz.')

    class Meta:
        app_label = 'personnelTransactions'


class CustomUser(AbstractUser):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True, null=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True)
    neighbourhood = models.CharField(max_length=100, blank=True, null=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions', blank=True
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups', blank=True
    )


class Personnel(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(("date joined"), default=timezone.now)
    updated_at = models.DateTimeField(("date joined"), default=timezone.now)

    class Meta:
        app_label = 'personnelTransactions'
