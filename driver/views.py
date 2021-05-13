from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import Article
from .serializers import ArticleSerializer
import driver.s3_bucket as s3
# Create your views here.

class ArticleView(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticated,)


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        s3.upload_file('static/driver/file/text.txt', 'khugle-drive-test2', 'image/test.txt')
