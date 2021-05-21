from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import Article
from .serializers import ArticleSerializer
import driver.s3_bucket as s3
import os
from django.conf import settings
# Create your views here.

class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        file_path = serializer.data.get('file')
        file_name = file_path.split('/')[-1]
        s3.upload_file(os.path.join(settings.MEDIA_ROOT, file_name), 'khugle-drive-test', 'image/test2.txt')