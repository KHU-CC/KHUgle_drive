from django.db import models

# Create your models here.
class File(models.Model):
    """Model representing file to upload or download"""
    
    file = models.FileField()
    file_name = models.CharField(max_length=144)
    path = models.CharField(max_length=1000)
    