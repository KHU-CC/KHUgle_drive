from django.urls import path, include
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
    path('private/<path:folder_path>', views.private_bucket_file, name='private_bucket_file'),
    path('group', views.group_bucket, name='group_bucket'),
    path('group/<path:folder_path>', views.group_bucket_file, name='group_bucket_file'),
]