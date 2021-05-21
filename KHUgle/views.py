from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Post
from .forms import PostForm

def index(request):
    """커뮤니티 인덱스 페이지"""
    post_list = Post.objects.order_by('-created_at')  #post_list는 생성 시간 역순 정렬
    context = {'post_list': post_list}                  #context의 'post_list' 키에 담기
    
    return render(request, 'KHUgle/post_list.html', context)   #해당 html를 불러오며 context 전송


def detail(request, post_id):
    """커뮤니티에 포스팅 된 글에 접속한 페이지"""
    post = get_object_or_404(Post, pk=post_id)             # DB에서 가져온다.
    context = {'post':post}

    return render(request, 'KHUgle/post_detail.html', context)


def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.save()
            return redirect('KHUgle:index')
    else:
        form = PostForm()
    context = {'form': form}
    return render(request, 'KHUgle/post_form.html', context)