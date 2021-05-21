from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import viewsets
from .views import FileView

app_name = 'bucket'

file_list = FileView.as_view({
    'post': 'upload',
    'get': 'list',
})

file_detail = FileView.as_view({
    'get': 'download',
    'patch': 'move',
    'delete': 'destroy',
})

urlpatterns = format_suffix_patterns([
    path('file/', file_list, name='file_list'),
    path('file/<int:pk>', file_detail,name='file_detail'),
])