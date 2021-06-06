from django.urls import path, include
from . import views

app_name = 'bucket'

urlpatterns = [
    path('private/file', views.private_bucket, name='private_bucket'),
    path('private/file/<path:folder_path>', views.private_bucket_file, name='private_bucket_file'),
    path('private/download/<path:file_path>', views.private_download, name='private_download'),
    path('private/delete/<path:file_path>', views.private_file_delete, name='private_file_delete'),
    path('private/create', views.private_bucket_create, name='private_bucket_create'),
    path('private/create/<path:folder_path>', views.private_folder_create, name='private_folder_create'),
    path('private/download/<path:file_path>', views.private_download, name='private_download'),
    path('group/file', views.group_bucket, name='group_bucket'),
    path('group/file/<path:folder_path>', views.group_bucket_file, name='group_bucket_file'),
    path('group/download/<path:file_path>', views.group_download, name='group_download'),
    path('group/delete/<path:file_path>', views.group_file_delete, name='group_file_delete'),
    path('group/create', views.group_bucket_create, name='group_bucket_create'),
    path('group/create/<path:folder_path>', views.group_folder_create, name='group_folder_create'),
]