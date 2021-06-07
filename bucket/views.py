from KHUgle.models import Post
from django.shortcuts import render
from KHUgle.forms import DeletePostForm
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.views.decorators.csrf import csrf_exempt
from .models import File
from django.http import JsonResponse
from .serializer import FileSerializer
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
import bucket.s3_work as s3
import os
from django.core.files.storage import FileSystemStorage

# Create your views here.
@csrf_exempt
@login_required(login_url='account:login')
def private_bucket(request):
    permission_classes = (permissions.IsAuthenticated,)
    user = request.user
    bucket_private = 'khugle-drive-' + user.username

    if request.method == 'GET':
        file_list = s3.list_object('khugle-drive-' + user.username, '', user)
        return render(request, 'bucket/private_bucket.html', {'file_list' : file_list})

    if request.method == 'POST' and request.FILES['upload']:
        myfile = request.FILES['upload']
        fs = FileSystemStorage("static/files")
        filename = fs.save(myfile.name, myfile)
        # uploaded_file_url = fs.url(filename)
        print(filename)
        # filename = str(filename)
        s3.upload_file(filename, 'khugle-drive-'+request.user.username)
        file_list = s3.list_object('khugle-drive-' + user.username, '', user)
        return render(request, 'bucket/private_bucket.html', {'file_list' : file_list})

@csrf_exempt
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

    if request.method == 'POST' and request.FILES['upload']:
        myfile = request.FILES['upload']
        folders = folder_path.split('/')
        folder_path = ''

        for i in range(len(folders)-1):
            folder_path += folders[i] + '/'
        fs = FileSystemStorage("static/files")
        filename = fs.save(myfile.name, myfile)
        
        print(filename)
        
        s3.upload_file(filename, 'khugle-drive-'+request.user.username, folder_path+filename)
        file_list = s3.list_object('khugle-drive-' + user.username, folder_path, user)
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

@csrf_exempt
@login_required(login_url='account:login')
def private_bucket_create(request):
    user = request.user
    bucket_private = 'khugle-drive-' + user.username
    if request.method == 'POST':
        s3.make_directory(request.POST['bucket'], bucket_private, '')
    return redirect('/bucket/private/file')

@csrf_exempt
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
    bucket_major = 'khugle-drive-qwer2'
    #bucket_major = 'khugle-drive-' + user.major.lower()

    if request.method == 'GET':
        file_list = s3.list_object(bucket_major, '', user)
        return render(request, 'bucket/group_bucket.html', {'file_list' : file_list})

@login_required(login_url='account:login')
def group_bucket_file(request, folder_path):
    permission_classes = (permissions.IsAuthenticated,)
    user = request.user
    bucket_major = 'khugle-drive-qwer2'
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
    bucket_major = 'khugle-drive-qwer2'
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
def group_file_log(request, file_path):
    """커뮤니티 인덱스 페이지"""
    page = request.GET.get('page', '1')             # 페이지
    # kw = request.GET.get('kw', '')                  # 검색어
    # so = request.GET.get('so', 'recent')            # 정렬
    post_list = Post.objects.filter(file_path=file_path).order_by('-created_at')  #post_list는 생성 시간 역순 정렬
    print(post_list)
    # if so == 'recommend':
    #     post_list = Post.objects.filter(major=request.user.major).annotate(num_voter=Count('voter')).order_by('-num_voter', '-created_at')
    # elif so == 'popular':
    #     post_list = Post.objects.filter(major=request.user.major).annotate(num_comment=Count('comment')).order_by('-num_comment', '-created_at')
    # else:
    #     post_list = Post.objects.filter(major=request.user.major).order_by('-created_at')

    # if kw:
    #     post_list = post_list.filter(
    #         Q(title__icontains=kw) |
    #         Q(content__icontains=kw) |
    #         Q(author__username__icontains=kw) |
    #         Q(comment__author__username__icontains=kw)
    #     ).distinct()

    paginator = Paginator(post_list, 10)            # 페이지에 10개씩 묶기
    page_obj = paginator.get_page(page)
    context = {'post_list': page_obj, 'file_path': file_path, 'page':page}               # page_obj를 불러오기
                                                    # 불러오는 방식 --> localhost:8000/KHUgle/?page=1
    
    return render(request, 'KHUgle/post_log.html', context)   #해당 html를 불러오며 context 전송

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
            s3.delete_file(file_path, 'khugle-drive-qwer2')
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

@csrf_exempt
@login_required(login_url='account:login')
def group_bucket_create(request):
    user = request.user
    bucket_major = 'khugle-drive-qwer2'
    #bucket_major = 'khugle-drive-' + user.major.lower()
    if request.method == 'POST':
        s3.make_directory(request.POST['bucket'], bucket_major, '')
    return redirect('/bucket/group/file')

@csrf_exempt
@login_required(login_url='account:login')
def group_folder_create(request, folder_path):
    user = request.user
    bucket_major = 'khugle-drive-qwer2'
    #bucket_major = 'khugle-drive-' + user.major.lower()
    if request.method == 'POST':
        s3.make_directory(folder_path + request.POST['folder'], bucket_major, '')
    return redirect('/bucket/group/file/' + folder_path)

@csrf_exempt
@login_required(login_url='account:login')
def private_upload_file(request):
    if request.method == 'POST':
        print(request)