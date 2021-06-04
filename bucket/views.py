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
    user = request.user
    bucket_private = 'khugle-drive-' + user.username

    if request.method == 'GET':
        file_list = s3.list_object('khugle-drive-' + user.username, '', user)
        return render(request, 'bucket/private_bucket.html', {'file_list' : file_list})

    else :
        print('DELETE')


@api_view(['GET', 'PUT', 'DELETE'])
def private_bucket_file(request, folder_path):
    permission_classes = (permissions.IsAuthenticated,)
    user = request.user
    bucket_private = 'khugle-drive-' + user.username

    if request.method == 'GET':
        folders = folder_path.split('/')
        folder_path = ''
        for i in range(len(folders)-1):
            folder_path += folders[i] + '/'
        file_list = s3.list_object(bucket_private, folder_path, user)
        return render(request, 'bucket/private_bucket_file.html', {'file_list' : file_list, 'current_path' : folder_path})
    
    elif request.method == 'DELETE' :
        print('DELETE')

def private_file_delete(request, file_path):
    user = request.user
    bucket_private = 'khugle-drive-' + user.username
    s3.delete_file(file_path, bucket_private)

def private_bucket_create(request):
    user = request.user
    bucket_private = 'khugle-drive-' + user.name
    s3.make_directory(request.directory_name, bucket_private, '')

def private_folder_create(request, folder_path):
    user = request.user
    bucket_private = 'khugle-drive-' + user.name
    s3.make_directory(request.directory_name, bucket_private, folder_path)

@api_view(['GET','POST'])
def group_bucket(request):
    permission_classes = (permissions.IsAuthenticated,)
    user = request.user
    bucket_major = 'khugle-drive-qwer'
    #bucket_major = 'khugle-drive-' + user.major.lower()

    if request.method == 'GET':
        file_list = s3.list_object(bucket_major, '', user)
        return render(request, 'bucket/group_bucket.html', {'file_list' : file_list})

    else :
        print('POST')

@api_view(['GET', 'PUT', 'DELETE'])
def group_bucket_file(request, folder_path):
    permission_classes = (permissions.IsAuthenticated,)
    user = request.user
    print(str(request))
    bucket_major = 'khugle-drive-qwer'
    #bucket_major = 'khugle-drive-' + user.major.lower()

    if request.method == 'GET':       
        folders = folder_path.split('/')
        folder_path = ''
        for i in range(len(folders)-1):
            folder_path += folders[i] + '/'
        file_list = s3.list_object(bucket_major, folder_path, user)
        return render(request, 'bucket/group_bucket_file.html', {'file_list' : file_list, 'current_path' : folder_path})
    
    elif request.method == 'DELETE' :
        print('DELETE')

    else:
        print('PUT')

def group_file_delete(request, file_path):
    user = request.user
    bucket_major = 'khugle-drive-qwer'
    #bucket_major = 'khugle-drive-' + user.major.lower()
    s3.delete_file(file_path, bucket_major)

def group_bucket_create(request):
    user = request.user
    bucket_major = 'khugle-drive-qwer'
    #bucket_major = 'khugle-drive-' + user.major.lower()
    s3.make_directory(request.directory_name, bucket_major, '')

def group_folder_create(request, folder_path):
    user = request.user
    bucket_major = 'khugle-drive-qwer'
    #bucket_major = 'khugle-drive-' + user.major.lower()
    s3.make_directory(request.directory_name, bucket_major, folder_path)

#@api_view(['GET'])
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
