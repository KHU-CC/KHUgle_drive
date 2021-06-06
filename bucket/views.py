from django.shortcuts import render
from KHUgle.forms import DeletePostForm
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from .models import File
from django.http import JsonResponse
from .serializer import FileSerializer
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
import bucket.s3_work as s3
import os

# Create your views here.
@login_required(login_url='account:login')
def private_bucket(request):
    permission_classes = (permissions.IsAuthenticated,)
    user = request.user
    bucket_private = 'khugle-drive-' + user.username

    if request.method == 'GET':
        file_list = s3.list_object('khugle-drive-' + user.username, '', user)
        return render(request, 'bucket/private_bucket.html', {'file_list' : file_list})

@login_required(login_url='account:login')
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

@login_required(login_url='account:login')
def private_download(request, file_path):
    user = request.user
    bucket_private = 'khugle-drive-' + user.username
    print("file_path : "+ file_path)
    s3.download_file(bucket_private, file_path, 'static/files')
    folders = file_path.split('/')
    if len(folders) == 1:
        return redirect('/bucket/private/file')
    new_path = '/'
    for i in range(len(folders) - 1):
        new_path += folders[i]
        new_path += '/'
    return redirect('/bucket/private/file' + new_path)

@login_required(login_url='account:login')
def private_file_delete(request, file_path):
    user = request.user
    bucket_private = 'khugle-drive-' + user.username
    #bucket_major = 'khugle-drive-' + user.major.lower()
    print("file_path : "+ file_path)
    s3.delete_file(file_path, bucket_private)
    folders = file_path.split('/')
    if len(folders) == 1:
        return redirect('/bucket/private/file')
    new_path = '/'
    for i in range(len(folders) - 1):
        new_path += folders[i]
        new_path += '/'
    return redirect('/bucket/private/file' + new_path)

@login_required(login_url='account:login')
def private_bucket_create(request):
    user = request.user
    bucket_private = 'khugle-drive-' + user.username
    if request.method == 'POST':
        s3.make_directory(request.POST['bucket'], bucket_private, '')
    return redirect('/bucket/private/file')

@login_required(login_url='account:login')
def private_folder_create(request, folder_path):
    user = request.user
    bucket_private = 'khugle-drive-' + user.username
    if request.method == 'POST':
        print(folder_path + request.POST['folder'])
        s3.make_directory(folder_path + request.POST['folder'], bucket_private, '')
    return redirect('/bucket/private/file/' + folder_path)

@login_required(login_url='account:login')
def group_bucket(request):
    permission_classes = (permissions.IsAuthenticated,)
    user = request.user
    bucket_major = 'khugle-drive-qwer'
    #bucket_major = 'khugle-drive-' + user.major.lower()

    if request.method == 'GET':
        file_list = s3.list_object(bucket_major, '', user)
        return render(request, 'bucket/group_bucket.html', {'file_list' : file_list})

@login_required(login_url='account:login')
def group_bucket_file(request, folder_path):
    permission_classes = (permissions.IsAuthenticated,)
    user = request.user
    bucket_major = 'khugle-drive-qwer'
    #bucket_major = 'khugle-drive-' + user.major.lower()      
    folders = folder_path.split('/')
    folder_path = ''
    for i in range(len(folders)-1):
        folder_path += folders[i] + '/'
    file_list = s3.list_object(bucket_major, folder_path, user)
    return render(request, 'bucket/group_bucket_file.html', {'file_list' : file_list, 'current_path' : folder_path})

@login_required(login_url='account:login')
def group_download(request, file_path):
    user = request.user
    bucket_major = 'khugle-drive-qwer'
    print("file_path : "+ file_path)
    s3.download_file(bucket_major, file_path, 'static/files')
    folders = file_path.split('/')
    if len(folders) == 1:
        return redirect('/bucket/major/file')
    new_path = '/'
    for i in range(len(folders) - 1):
        new_path += folders[i]
        new_path += '/'
    return redirect('/bucket/major/file' + new_path)

@login_required(login_url='account:login')
def group_file_delete(request, file_path):

    form = DeletePostForm()
    
    if request.method == 'POST':
        form = DeletePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_at = timezone.now()
            post.major = request.user.major
            post.save()
            s3.delete_file(file_path, 'khugle-drive-qwer')
            #s3.delete_file(file_path, 'khugle-drive-' + request.user.major)
            folders = file_path.split('/')
            if len(folders) == 1:
                return redirect('/bucket/group/file')
            new_path = '/'
            for i in range(len(folders) - 1):
                new_path += folders[i]
                new_path += '/'
            return redirect('/bucket/group/file' + new_path)
    context = {'form': form}
    return render(request, 'KHUgle/post_form.html', context)

@login_required(login_url='account:login')
def group_bucket_create(request):
    user = request.user
    bucket_major = 'khugle-drive-qwer'
    #bucket_major = 'khugle-drive-' + user.major.lower()
    if request.method == 'POST':
        s3.make_directory(request.POST['bucket'], bucket_major, '')
    return redirect('/bucket/group/file')

@login_required(login_url='account:login')
def group_folder_create(request, folder_path):
    user = request.user
    bucket_major = 'khugle-drive-qwer'
    #bucket_major = 'khugle-drive-' + user.major.lower()
    if request.method == 'POST':
        s3.make_directory(folder_path + request.POST['folder'], bucket_major, '')
    return redirect('/bucket/group/file/' + folder_path)