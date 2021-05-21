from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ArticleView


article_list = ArticleView.as_view({
    'post': 'create',
    'get': 'list',
})


article_detail = ArticleView.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = format_suffix_patterns([
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('articles/', article_list, name='article_list'),
    path('articles/<int:pk>', article_detail, name='article_detail'),
])
