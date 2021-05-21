from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import File
from .serializer import FileSerializer
from django.conf import settings
import bucket.s3_work as s3
import os
# Create your views here.
class FileView(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def upload(self, serializer, file_path, file_name):
        
        serializer.save()
        file_path = serializer.data.get('file')
        file_name = file_path.split('/')[-1]
        s3.upload_file(os.path.join(settings.MEDIA_ROOT, file_name), 'khugle-drive-admin', file_path + file_name)
    
    def list(self, serializer):
        return

    def download(self, serializer):
        return
    
    def move(self, seiralizer):
        return

    def destroy(self, serializer):
        return

    