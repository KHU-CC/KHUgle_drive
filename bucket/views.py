from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from .models import File
from django.http import JsonResponse
from .serializer import FileSerializer
from django.conf import settings
import bucket.s3_work as s3
import os
# Create your views here.


@api_view(['GET','POST'])
def private_bucket(request):
    permission_classes = (permissions.IsAuthenticated,)
    if request.method == 'GET':
        user = request.user
        file_list = s3.list_object('khugle-drive-' + user.username, '', user)
        print(file_list)
        return render(request, 'bucket/private_bucket.html', {'file_list' : file_list})
    
    else :
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            file_path = serializer.data.get('file')
            file_name = file_path.split('/')[-1]
            user = request.user
            s3.upload_file(os.path.join(settings.MEDIA_ROOT, file_name), 'khugle-drive-'+user.username, file_path + file_name)
            return JsonResponse(serializer.data, status=201)


@api_view(['GET', 'PUT', 'DELETE'])
def private_bucket_file(request, path='/'):
    #file = get_object_or_404(File, path=path)
    if request.method == 'GET':
        user = request.user
        print('path : ' + request.path)
        file_list = s3.list_object('khugle-drive-' + user.username, path, user)
        return render(request, 'bucket/private_bucket_file.html', {'file_list' : file_list})
    
    elif request.method == 'DELETE' :
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            file_path = serializer.data.get('file')
            file_name = file_path.split('/')[-1]
            user = request.user
            s3.upload_file(os.path.join(settings.MEDIA_ROOT, file_name), 'khugle-drive-'+user.username, file_path + file_name)
            return JsonResponse(serializer.data, status=201)

@api_view(['GET','POST'])
def group_bucket(request):
    permission_classes = (permissions.IsAuthenticated,)
    if request.method == 'GET':
        user = request.user
        print(request.user)
        file_list = s3.list_object('khugle-drive-' + user.major.lower(), '','user')
        print(file_list)
        
        return render(request, 'bucket/group_bucket.html', {'file_list' : file_list})
    else :
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            file_path = serializer.data.get('file')
            file_name = file_path.split('/')[-1]
            user = request.user
            s3.upload_file(os.path.join(settings.MEDIA_ROOT, file_name), 'khugle-drive-'+user.magjo.lower(), file_path + file_name)
            return JsonResponse(serializer.data, status=201)

# class FileView(viewsets.ModelViewSet):
#     queryset = File.objects.all()
#     serializer_class = FileSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     @action(detail=False, method=['post'])
#     def upload(self, serializer):
#         if serializer.is_valid():
#             serializer.save()
#             file_path = serializer.data.get('file')
#             file_name = file_path.split('/')[-1]
#             s3.upload_file(os.path.join(settings.MEDIA_ROOT, file_name), 'khugle-drive-admin', file_path + file_name)
#             return JsonResponse(serializer.data, status=201)

#     @action(detail=False, method=['get'])
#     def list_files(self, serializer):
#         folder_list, file_list = s3.list_object(s3.BUCKET);
#         files = folder_list + file_list
#         return render(serializer, 'bucket/file_list.html', {'files' : files})

#     def download(self, serializer):
        
#         return
    
#     def move(self, seiralizer):
#         return

#     def destroy(self, serializer):
#         return
