import boto3
import logging
import json
import os
from django.conf import settings 
from botocore.exceptions import ClientError

# BASE_DIR = settings.BASE_DIR
# MEDIA_DIR = settings.MEDIA_ROOT
s3 = boto3.client(
    's3',
    aws_access_key_id='ASIARPQAACLCVB3VOU6J',
    aws_secret_access_key='b6nByzy3XPKjlmRWNtozrM6I8EYfG1K0QX5LzsH/',
    aws_session_token='IQoJb3JpZ2luX2VjEBgaCXVzLXdlc3QtMiJHMEUCIAlY0KbRobA5jX9wmdzTILUIIvt8HltxjwWomQkwqQidAiEAva3RTBVReo8cbN2stAEtD/c5I+fNoKUQfjvQRccw78wqtAIIwP//////////ARAAGgwxMDIwMDU0NzgwODUiDMR/i0Yxut8YCED7LiqIAjT5ziWPoIUk17QQKiYdxGdgob0y3rBJaQMsYFh0CouehwRCUizAygkbiEjM/AF6Fx+fzq44I93ZVTQ9ocancouDYqO1cLnTTTM8vFaddSAHqeD7Tudh7VqkTiic6SWH/wlQFwDHoYwJTfd1XzsWrD8W+Gb6+hJ0FFXPlzUvSF3WOWNHiZJ4+tFiaEVlJWoykNDEgBWfdYj9+QNVe+Y9Q9NcETmcsiNoR++bEfkrD6XSIMSsqldizfn3DmJfb9D0WzPaEgTj7wBdd+K3fAVYXCNa3WM76cTO6/p8mTGfmuxSw9US2/WfNhKBgfElOncuHvtPFsqcJ61naJ3+nrflqriDZ9XyPAvElTCqn9mFBjqdAaYKTsN26VkQHXhe21unfbmc5KxOiEU7043NiudD4AKbHl51eb2h3w8criS4YV6FTmsp1egyGxg6QZW/5fqRppMiU6cDsZr+YsTTKqjVkGKzasaXzT9g2uA1N+g7u9guRbcRCyWe0/K0ssolNYu7Ed8V/xjlx8sc0x07we4yinyMJCeG8mrAMBTN5koHgn4h9lR5YYSdAJengboG1EY=',
    region_name = 'us-east-1'
)

BUCKET = 'khugle-drive-admin'

def upload_file(file_name, bucket, file_path=None):
    # If S3 object_name was not specified, use file_name
    if file_path is None:
        file_path= file_name
    # Upload the fil
    response = s3.upload_file(file_name, bucket, file_path)
    return response

def list_object(bucket, folder_path, user):
    response = s3.list_objects(Bucket=bucket, Prefix=folder_path, Delimiter='/')
    print(response)
    file_list = []
    folder_res = response.get('CommonPrefixes')
    file_res = response.get('Contents')
    if folder_res:
        for folder in folder_res:
            file_list.append({'name': folder.get('Prefix').split('/')[-2], 'path': folder.get('Prefix'), 'is_folder': True, 'user' : user})
    if file_res:
        for file in file_res:
            file_list.append({'name': file.get('Key').split('/')[-1], 'path': file.get('Key'), 'is_folder': False, 'user':user})
    # file_list = folder_list + file_list
    print(file_list)
    return file_list


def download_file(bucket, file_path, download_path):
    response = s3.download_file(bucket, file_path, download_path)
    return response

def move_file(old_file_path, bucket, new_file_path):
    copy_source = {
        'Bucket': bucket,
        'Key' : old_file_path
    }
    s3.copy_object(Bucket=bucket, CopySource=copy_source, Key=new_file_path)

def rename_file(old_file_path, bucket, new_file_path):  
    copy_source = {
        'Bucket': bucket,
        'Key': old_file_path
    }
    s3.copy_object(Bucket=bucket, CopySource=copy_source, Key=new_file_path)
    s3.delete_object(Bucket=bucket, Key=old_file_path)

def delete_file(file_name, bucket):
    response = s3.delete_object(Bucket=bucket, Key=file_name)
    return response

def make_directory(dir_name, bucket, current_path):
    response = s3.put_object(Bucket=bucket, Key= current_path+dir_name+'/')
    return response

def create_bucket(bucket):
    response = s3.create_bucket(Bucket=bucket)
    return response

def update_path(path, folder):
    return path + '/' + 'folder'
