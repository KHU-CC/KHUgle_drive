from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework import viewsets
# from .views import FileView
from . import views

app_name = 'bucket'

# file_list = FileView.as_view({
#     'post': 'create',
#     'get': 'list',
# })

# file_detail = FileView.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partical_update',
#     'delete': 'destroy',
# })

urlpatterns = [
    path('private', views.private_bucket, name='private_bucket'),
    path('private/<str:path>', views.private_bucket_file, name='private_bucket_file'),
    path('group', views.group_bucket, name='group_bucket'),
]