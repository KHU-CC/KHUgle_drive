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
    aws_access_key_id='ASIAVJ7ZLDLC57AZDDF5',
    aws_secret_access_key='hmlbc8di7Muu1A0o/1Egpr3fktcUMwRFCi9jNZZF',
    aws_session_token='FwoGZXIvYXdzEHwaDJrvvSr6td8s47o9ByLCAXECfysMqXHsHPuW8mbyoiv8RX9Jgph2B38kNxP4pUbWKwZUrwUfyW6soMX4TvdLxCyn4jCYNtcpREbUpcarJbA9M1XYHEQvleWPQKuu20SVK7X8qLsxkdE4cuIrUnf4c7WdtlJTxh+RvKpZBAVdexb+76j4ckNM6IS6Bt0rcjCbuXoU3tb9vANBSjVsqDypxruunSs2LIPewCCAnpgfaKqmeJGD/8xvRw+B5tKFYZ/K8DUW/BB6++PeO/cclPF7uLe6KNDH64UGMi12kpd2L0nJkhvsnp/dFVym6Qv554lWwXI3PfAOW4Tf77oIqkz7zuLqkFVEUHE=',
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
