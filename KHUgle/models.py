from django.db import models
from account.models import CustomUser

# File model을 이용하여 file의 정보를 담는다. (file, filename, filepath)
# Notice model을 이용하여 file name을 기준으로 notice를 정리한다.
# Filelog model을 이용하여 notice와 연결하여 file의 변화 상태를 기록, 보여준다.
# Post model을 이용하여 community 기능을 한다.


# class File(models.Model):
#     file = models.FileField()
#     file_path = models.CharField(max_length=1000)
    
#     def __str__(self):
#         # shell에서 DB확인을 위해 출력 용도로 작성
#         return self.title



# class Notice(models.Model):
#     """Model representing the state of file from S3 bucket"""
#     file_id = models.ForeignKey(File)
    
#     def __str__(self):
#         # shell에서 DB확인을 위해 출력 용도로 작성
#         return self.title
    



# class Filelog(models.Model):
#     """Model representing the log of file from S3 bucket"""
#     notice = models.ForeignKey(Notice, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField()
    
#     def __str__(self):
#         # shell에서 DB확인을 위해 출력 용도로 작성
#         return self.title



class Post(models.Model):
    """Model representing community posts"""
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE) #커스텀 유저 모델과 연결
    title = models.CharField(max_length=144)
    content = models.TextField()
    file = models.FileField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(CustomUser, related_name='voter_post')

    def __str__(self):
        # shell에서 DB확인을 위해 출력 용도로 작성
        return self.title

class Comment(models.Model):
    """Model representing comment posts"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    voter = models.ManyToManyField(CustomUser, related_name='voter_comment')

    
