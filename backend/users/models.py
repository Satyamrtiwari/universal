from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Doctor'),
        ('PHARMACIST', 'Pharmacist'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PATIENT')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    area_village = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"
