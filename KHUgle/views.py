from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
import bucket.s3_work as s3

def main(request):
    """사이트 첫 페이지"""
    return render(request, 'KHUgle/main.html')


@login_required(login_url='account:login')
def index(request):
    """커뮤니티 인덱스 페이지"""
    page = request.GET.get('page', '1')             # 페이지
    kw = request.GET.get('kw', '')                  # 검색어
    so = request.GET.get('so', 'recent')            # 정렬
    post_list = Post.objects.order_by('-created_at')  #post_list는 생성 시간 역순 정렬

    if so == 'recommend':
        post_list = Post.objects.annotate(num_voter=Count('voter')).order_by('-num_voter', '-created_at')
    elif so == 'popular':
        post_list = Post.objects.annotate(num_comment=Count('comment')).order_by('-num_comment', '-created_at')
    else:
        post_list = Post.objects.order_by('-created_at')

    if kw:
        post_list = post_list.filter(
            Q(title__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(comment__author__username__icontains=kw)
        ).distinct()

    paginator = Paginator(post_list, 10)            # 페이지에 10개씩 묶기
    page_obj = paginator.get_page(page)
    context = {'post_list': page_obj, 'page':page, 'kw':kw, 'so':so}               # page_obj를 불러오기
                                                    # 불러오는 방식 --> localhost:8000/KHUgle/?page=1
    
    return render(request, 'KHUgle/post_list.html', context)   #해당 html를 불러오며 context 전송


@login_required(login_url='account:login')
def detail(request, post_id):
    """커뮤니티에 포스팅 된 글에 접속한 페이지"""
    post = get_object_or_404(Post, pk=post_id)             # DB에서 가져온다.
    context = {'post':post}

    return render(request, 'KHUgle/post_detail.html', context)


@login_required(login_url='account:login')
def post_create(request, folder_path):
    form = PostForm()
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        print(form)
        print(form.is_valid)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_at = timezone.now()
            post.save()
            print(str(request.FILES.get('file')))
            for file in form.files:
                 s3.upload_file(str(request.FILES.get('file')), 'khugle-drive-'+request.user.username, folder_path + str(request.FILES.get('file')))
            
            return redirect('bucket:private_bucket_file', folder_path=folder_path)
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'KHUgle/post_form.html', context)


@login_required(login_url='account:login')
def post_modify(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, 'Permission Error')
        return redirect('KHUgle:detail', post_id=post.id)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.updated_at = timezone.now()  # 수정일시 저장
            post.save()
            return redirect('KHUgle:detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    context = {'form': form}
    return render(request, 'KHUgle/post_form.html', context)


@login_required(login_url='account:login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        messages.error(request, 'Permission Error')
        return redirect('KHUgle:detail', post_id=post.id)
    post.delete()
    return redirect('KHUgle:index')


@login_required(login_url='account:login')
def comment_create(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if (request.method == "POST"):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.created_at = timezone.now()
            comment.author = request.user
            comment.save()
            redirect('KHUgle:detail', post_id=post_id)
    else:
        form = CommentForm()
    context = {'post':post, 'form':form}
    return render(request, 'KHUgle/post_detail.html', context)


@login_required(login_url='account:login')
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if (request.user != comment.author):
        messages.error(request, 'No Permission')
    else:
        comment.delete()
    return redirect('KHUgle:detail', post_id=comment.post.id)


@login_required(login_url='account:login')
def vote_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.voter.add(request.user)
    return redirect('KHUgle:detail', post_id=post.id)


@login_required(login_url='account:login')
def vote_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.voter.add(request.user)
    return redirect('KHUgle:detail', post_id=comment.post.id)