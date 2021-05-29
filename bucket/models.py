from django.db import models
from account.models import CustomUser

# Create your models here.
class File(models.Model):
    """Model representing file to upload or download"""
    is_folder = models.BooleanField(default=False)
    file = models.FileField()
    path = models.CharField(max_length=1000)
    user = models.CharField(max_length=100)