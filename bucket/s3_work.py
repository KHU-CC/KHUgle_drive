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
    aws_access_key_id='ASIAVJ7ZLDLC5XC4OO54',
    aws_secret_access_key='gAhoW+5p3E8vLpM8G8MKu1XrCb4PRXInzMHhRaI5',
    aws_session_token='FwoGZXIvYXdzEJT//////////wEaDEuYbSZuOUCCLav4CiLCAQFgws6B5hO1DbcQT5mmnT+z91SdT5rwnTuTRP04LKs9va91oakNHpQ9dvGtWsHQHY8/zrr8YCDN8CSULSviO9zKIOBPQmgTvuwUW+JGqU+HkGojtWJ/zG849lw5tpOe3VZ3a8PT+S5VgtRFCb3xjTfRz6VM6A1UDsTgEy1CCqjqvWUtSLsROXm7xtPrytiGwm57OwSJ+zJ63H8Nue+Zg5en2BmaePWm82Q2kF5W641s1dqsevF/+zkYSWw0egKu/Qp+KLfq8IUGMi1DtDqFa3ftej76dTIYBmQYlysaZsv0XsnUyLlwcuv30Q+jgQ5Szzq6q7bHZEc=',
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
            if file.get('Key').split('/')[-1] == '':
                continue
            file_list.append({'name': file.get('Key').split('/')[-1], 'path': file.get('Key'), 'is_folder': False, 'user':user})
    # file_list = folder_list + file_list
    print('file_list ' + bucket + ' path : ' + folder_path + ' ' + str(file_list))
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
    print('make_directory ' + bucket + ' : ',current_path+dir_name+'/')
    response = s3.put_object(Bucket=bucket, Key= current_path+dir_name+'/')
    return response

def create_bucket(bucket):
    response = s3.create_bucket(Bucket=bucket)
    return response

def update_path(path, folder):
    return path + '/' + 'folder'
