from django.db import models

# Create your models here.
class Account(models.Model):
    studentId = models.CharField(max_length = 10)
    email = models.CharField(max_length = 200)
    user_name = models.CharField(max_length = 500)
    user_id = models.CharField(max_length = 200)
    password = models.CharField(max_length = 500)
    course = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "accounts"