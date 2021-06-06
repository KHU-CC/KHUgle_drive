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
    aws_access_key_id='ASIAVJ7ZLDLCXJW24AE2',
    aws_secret_access_key='3SSe9BnTupsXhBcathrgz2MNECjrfLvBuwAAUQe+',
    aws_session_token='FwoGZXIvYXdzEKD//////////wEaDN1egTaBSBvi8SvQCiLCAUyPnXHb5unT7SF7E61h9LiVX+QERfryghnG6DQpBPd1YaXUkiK77iUdsbvQbEeM++2elNwOyoIU5iAIpN3EwQ1jMz03Iq22lGCLCA9OGwfckPZc58hAYh2Q/oXiJjj1/9VRVkRVBbR8WisRTwf4Uo9MQIqUKLfKodScbkjPKp3wCk3oX2floxsWAu3+R/ka88QJ6YhgwarPzbgVXehKAnQ3hMq6TuwZNNgAKmth9ZzK80w8sRdCx/uYfEEtPpibzKpiKKGy84UGMi0voCs05Z/mm/TbFbVFy0+EbwQgmoPAnSafrPkmU5hPTR7ys+RpHok2HALoWgU=',
    region_name = 'us-east-1'
)

BUCKET = 'khugle-drive-admin'

def upload_file(file_name, bucket, file_path=None):
    # If S3 object_name was not specified, use file_name
    if file_path is None:
        file_path= file_name
    # Upload the file
    response = s3.upload_file('static/files/' +file_name, bucket, file_path)
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
