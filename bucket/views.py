from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .models import File
from django.http import JsonResponse
from .serializer import FileSerializer
from django.conf import settings
import bucket.s3_work as s3
import os
# Create your views here.
class FileView(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def upload(self, serializer):
        if serializer.is_valid():
            serializer.save()
            file_path = serializer.data.get('file')
            file_name = file_path.split('/')[-1]
            s3.upload_file(os.path.join(settings.MEDIA_ROOT, file_name), 'khugle-drive-admin', file_path + file_name)
            return JsonResponse(serializer.data, status=201)

    def list(self, serializer, folder_path):
        folder_list, file_list = s3.list_object(s3.BUCKET, folder_path)
        return JsonResponse(serializer.data, status=201)

    def download(self, serializer):
        return
    
    def move(self, seiralizer):
        return

    def destroy(self, serializer):
        return
