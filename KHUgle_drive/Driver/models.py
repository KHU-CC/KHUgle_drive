from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.urls import reverse
from django.utils import timezone




class UserManager(BaseUserManager):
    def create_user(self, email, nickname, studentID, departmentID, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            nickname = nickname,
            studnetID = studentID,
            departmentID = departmentID
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, studentID, departmentID,, password):
        user = self.create_user(
            email,
            password=password,
            nickname = nickname,
            studnetID = studentID,
            departmentID = departmentID
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    #date_of_birth = models.DateField()
    nickname = models.CharField(

    )
    studnetID = models.CharField(

    )
    departmentID = models.CharField(

    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['date_of_birth']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


# Create your models here.
class Article(models.Model):
    """Model representing community articles."""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=500, help_text='Enter a title')
    content = models.TextField(max_length=1000, help_text='Enter a brief content message')
    #comment_count =
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #like_count =
    #view_count =
    department_id = models.ForeignKey('Department', null=True)

class Comment(models.Model):
    """Model representing article comments."""
    author = models.ForiegnKey(User, on_delete=CASCADE)
    article_id = models.ForiegnKey(Article, on_delete=CASCADE)
    content = models.TextField(max_length=500, help_text='Enter a comment')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

