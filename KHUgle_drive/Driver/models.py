from django.db import models
from django.urls import reverse
from django.utils import timezone
import uuid


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