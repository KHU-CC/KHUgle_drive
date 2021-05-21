from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    MAJORS = (
        ('1', 'Computer Science'),
        ('2', 'International Studies'),
        ('3', 'Chemical Engineering')
    )
    major = models.CharField(max_length=144, choices=MAJORS)