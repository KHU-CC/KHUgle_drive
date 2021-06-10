from KHUgle.models import Post
from django.shortcuts import render
from KHUgle.forms import DeletePostForm
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, renderers
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.core.paginator import Paginator
from django.contrib import messages
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

    if request.method == 'POST':
        try:
            myfile = request.FILES['upload']

            if s3.check_file_exist(bucket_private, '', myfile):
                messages.info(request, "이미 존재하는 파일입니다.")
                return redirect('/bucket/private/file')

            fs = FileSystemStorage("static/files")
            filename = fs.save(myfile.name, myfile)
            print(filename)
            messages.info(request, "성공적으로 파일을 저장했습니다.")
            s3.upload_file(filename, 'khugle-drive-'+request.user.username)
            file_list = s3.list_object('khugle-drive-' + user.username, '', user)
            return render(request, 'bucket/private_bucket.html', {'file_list' : file_list})
        except:
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

    if request.method == 'POST':
        try:
            myfile = request.FILES['upload']

            if s3.check_file_exist(bucket_private, folder_path, myfile):
                messages.info(request, "이미 존재하는 파일입니다.")
                return redirect('/bucket/private/file/' + folder_path)

            folders = folder_path.split('/')
            folder_path = ''
            for i in range(len(folders)-1):
                folder_path += folders[i] + '/'
            fs = FileSystemStorage("static/files")
            filename = fs.save(myfile.name, myfile)
            
            s3.upload_file(filename, 'khugle-drive-'+request.user.username, folder_path+filename)
            file_list = s3.list_object('khugle-drive-' + user.username, folder_path, user)
            return render(request, 'bucket/private_bucket_file.html', {'file_list' : file_list, 'current_path' : folder_path})
        except:
            file_list = s3.list_object('khugle-drive-' + user.username, folder_path, user)
            return render(request, 'bucket/private_bucket_file.html', {'file_list' : file_list, 'current_path' : folder_path})

@login_required(login_url='account:login')
def private_download(request, file_path):
    user = request.user
    bucket_private = 'khugle-drive-' + user.username
    print("file_path : "+ file_path)

    if settings.USER_OS == 'Windows':
        download_path = settings.WINDOWS_DOWNLOAD_PATH
    elif settings.USER_OS == "Darwins":
        download_path = settings.MAC_DOWNLOAD_PATH

    folders = file_path.split('/')
    file_name = folders[-1]

    s3.download_file(bucket_private, file_path, download_path + '/' + file_name)

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
        if not s3.check_folder_exist(bucket_private, folder_path, request.POST['folder']):   
            print(folder_path + request.POST['folder'])
            s3.make_directory(folder_path + request.POST['folder'], bucket_private, '')
            messages.info(request, '성공적으로 폴더를 생성했습니다.')
        else:
            messages.info(request, '이미 존재하는 폴더입니다.')
    return redirect('/bucket/private/file/' + folder_path)

@login_required(login_url='account:login')
def group_bucket(request):
    permission_classes = (permissions.IsAuthenticated,)
    user = request.user
    bucket_major = 'khugle-drive-testtesttest'
    #bucket_major = 'khugle-drive-' + user.major.lower()

    if request.method == 'GET':
        file_list = s3.list_object(bucket_major, '', user)
        return render(request, 'bucket/group_bucket.html', {'file_list' : file_list})

@login_required(login_url='account:login')
def group_bucket_file(request, folder_path):
    permission_classes = (permissions.IsAuthenticated,)
    user = request.user
    bucket_major = 'khugle-drive-testtesttest'
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
    bucket_major = 'khugle-drive-testtesttest'

    print("file_path : "+ file_path)

    if settings.USER_OS == 'Windows':
        download_path = settings.WINDOWS_DOWNLOAD_PATH
    elif settings.USER_OS == "Darwins":
        download_path = settings.MAC_DOWNLOAD_PATH

    folders = file_path.split('/')
    file_name = folders[-1]

    s3.download_file(bucket_major, file_path, download_path + '/' + file_name)

    folders = file_path.split('/')
    if len(folders) == 1:
        return redirect('/bucket/group/file')
    new_path = '/'
    for i in range(len(folders) - 1):
        new_path += folders[i]
        new_path += '/'
    
    return redirect('/bucket/group/file' + new_path)

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

    # 해당 파일에 대한 글을 쓴 user와 현재 user가 같으면 Delete가능
    folders = file_path.split('/')
    new_path = '/'
    for i in range(len(folders) - 1):
        new_path += folders[i]
        new_path += '/'

    post_list = Post.objects.filter(file_path=file_path)
    print(post_list)
    if len(post_list) == 0 or request.user != post_list[0].author:
        print("True")
        messages.info(request, "업로드한 유저만 파일을 삭제할 수 있습니다.")
        if len(folders) == 1:
            return redirect('/bucket/group/file')
        return redirect('/bucket/group/file' + new_path)

    form = DeletePostForm()
    
    if request.method == 'POST':

        form = DeletePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_at = timezone.now()
            post.major = request.user.major
            post.save()
            s3.delete_file(file_path, 'khugle-drive-testtesttest')
            #s3.delete_file(file_path, 'khugle-drive-' + request.user.major)
            if len(folders) == 1:
                return redirect('/bucket/group/file')
            return redirect('/bucket/group/file' + new_path)
    context = {'form': form}
    return render(request, 'KHUgle/post_form.html', context)

@csrf_exempt
@login_required(login_url='account:login')
def group_bucket_create(request):
    user = request.user
    bucket_major = 'khugle-drive-testtesttest'
    #bucket_major = 'khugle-drive-' + user.major.lower()
    if request.method == 'POST':
        if not s3.check_folder_exist(bucket_major, '', request.POST['folder']):   
            print(request.POST['folder'])
            s3.make_directory(request.POST['folder'], bucket_major, '')
            messages.info(request, '성공적으로 폴더를 생성했습니다.')
        else:
            messages.info(request, '이미 존재하는 폴더입니다.')
    return redirect('/bucket/group/file')

@csrf_exempt
@login_required(login_url='account:login')
def group_folder_create(request, folder_path):
    user = request.user
    bucket_major = 'khugle-drive-testtesttest'
    #bucket_major = 'khugle-drive-' + user.major.lower()
    if request.method == 'POST':
        if not s3.check_folder_exist(bucket_major, folder_path, request.POST['folder']):   
            print(folder_path + request.POST['folder'])
            s3.make_directory(folder_path + request.POST['folder'], bucket_major, '')
            messages.info(request, '성공적으로 폴더를 생성했습니다.')
        else:
            messages.info(request, '이미 존재하는 폴더입니다.')
    return redirect('/bucket/group/file/' + folder_path)

@csrf_exempt
@login_required(login_url='account:login')
def private_upload_file(request):
    if request.method == 'POST':
        print(request)