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
    aws_access_key_id='ASIAVJ7ZLDLC3C3NEHP7',
    aws_secret_access_key='owH6sTSzRLsW4RRs3aMyP5EMnTqg0kkT0wywyLIy',
    aws_session_token='IQoJb3JpZ2luX2VjEEoaCXVzLXdlc3QtMiJHMEUCIQDaRePagdSUqMfcAazqyT2AEVDslT1KKSjQuF+m/p/5DAIgOfOCEEc1S8wDLnkAtlz3tgQHj3iYP4Im/chbihPjxXgqtAII8///////////ARAAGgwzNjUwNTgyNjc4NDUiDJttg8PqQOzj9ODauiqIAsacO6L+LFAjb4Grl6UuiwIHcu1StXkx3uwmbNx8shn4mDMNgU7fCPH9RQe3+VRDPjDGL5bbvLcC+gL0CTbneA40Jz3bKCKHkQA25hr+XW9rdpJaNUeGMY4ZOJKFAo0YsC4Yg3jMFSz1CWbIJ7/mPNEzkKyBtYfIsCBxjClsOZqkVvBJVfpE+iOn+cLx7Qrdva43MVIo9wzRXv6Ua437n+1SwK7oqeISBcgeMg/pqL+aLj0KwmFcI6wgErIAfDJPFhNXJ0bOFrc6M3LCwdsR5ccWrOaGZzSyoh296Zt3P4H+A+q8nhgWBRXZfh+KczBQLp6kjQb/F/M9+IlwpssqEvX5hEGJEqYh6TCbp+SFBjqdAdGPRKgzu2P21crBvque0HaWo3dqXtUipBkwhNWEzLq8fUAwF6HQOOjj1wq8AdG5LQv6ICFBaJ+YYIFrJ4bg8XrfmEH4298xzswR7gQ7SB/pm/MUdjcxnhp516CARHDKjDviEhqY2iD/PDE6pmAOh6+JdrtcgPYuVeZnI07pS7Rhn1j7ddnzcGBojuMWcCBlwjGt43YvsaIDH5YNYaU=',
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
