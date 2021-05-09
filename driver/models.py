from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    """Model representing community articles."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=144, help_text='Enter a title')
    content = models.TextField(help_text='Enter a brief content message')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #like_count =
    #view_count =
    # department_id = models.ForeignKey('Department', null=True)

    def __str__(self):
        return '[{}] {}'.format(self.user.username, self.title)

# class Department(models.Model):
#     """Model representing department imformation."""
#     name = models.CharField(max_length = 200)
#     detail = models.TextField(max_length = 500, help_text='Enter a brief department introduction')
#     bucket_url = models.CharField(max_length = 500)
