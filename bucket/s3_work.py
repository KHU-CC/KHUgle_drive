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
    aws_access_key_id='ASIARPQAACLCUAWJSMLX',
    aws_secret_access_key='S3Vo4VAHLguTJS/Ma2YoeXO6Iigevhe/eCYS8uhv',
    aws_session_token='IQoJb3JpZ2luX2VjEOL//////////wEaCXVzLXdlc3QtMiJHMEUCIQCSAFpbcTrmrr5iMaHKf0qSU0RXc+0PCLxJZgOOJIcmAQIgfZF8+VJkPutN+Lq9DIagQZmXd+3X8IN6Sqx29EK4zHUqtAIIi///////////ARAAGgwxMDIwMDU0NzgwODUiDINJ3PIKfZQjYzxKBiqIAnfw3BvLQ3Cd92xghyKEvxBy3EHqAaxuiq64XNB/aH9H3eXf/9FBExZ5D9K7uwxgX/9g7FxBy5cnbspu0LlM86fgWSuMxNov6vJG+PCkLJMnQvZ4ujOJolX+uAlwPM2JooVZyML0npz9zMFGAKgSeZdccwjGKv62WFsHa+ZL/uelsIO3qp2Se2JOy6rL1HmTsPebHqUJr7wX6Y23E+TsR8Ky0hUWMpMGugXZ0z/fBUP0aN1XhKDgbePADcpKphb6ZeuOuGu0BH8PCyDP6scU8fyZMq5Ap9PFoFA7HQpquicSN/RTAgQcHKU2cwz2fconQJCjm9PsHxtOmPULCmvMT7nvJddm6PLN+jCYyc2FBjqdAY4Af7I5uEGHCks2kFK5/phIC5jL0q2wYXzOV+2DVy8QUO5vugWrkb6kuaENQpeYrOm+JE6jMzdi4mZVptnjijEY4UvOlbk8FtfLHUrVJj7sFV6zIJde+TEX0ysjNxPzHMBd4hlTV4PhADzqxn2DvDeEFJuD81qIhh1wkM3kVKWuT2+dNeRRL10oZlrwCOBdPcC9JamRBknxMwlwSn4=',
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
    print("folder_path: ", folder_path)

    response = s3.list_objects(Bucket=bucket)
    # print("response: ", response)
    file_list = []
    folder_list = {}
    folder_res = response.get('CommonPrefixes')
    file_res = response.get('Contents')
    if folder_res:
        for folder in folder_res:
            file_list.append({'name': folder.get('Prefix').split('/')[-2], 'path': folder.get('Prefix'), 'is_folder': True, 'user' : user})
    if file_res:
        for file in file_res:
            file_list.append({'name': file.get('Key').split('/')[-1], 'path': file.get('Key'), 'is_folder': False, 'user':user})
    # print("file_list: ", file_list)

    for file in file_list:
        if file['path'].find('/') != -1:
            path = file['path'][0:file['path'].rfind('/')]
            folder = file['path'].split('/')[-2]
            folder_list[folder] = path

    # for folder in folder_list:
    #     print("folder: ", folder, ": ", folder_list[folder])

    # print("folder_path", folder_path)
    if folder_path in folder_list:
        # print("this: ", folder_list[folder_path])
        folder_path = folder_list[folder_path]+'/'

    response = s3.list_objects(Bucket=bucket, Prefix=f'{folder_path}', Delimiter='/')
    file_list = []
    folder_res = response.get('CommonPrefixes')
    file_res = response.get('Contents')
    if folder_res:
        for folder in folder_res:
            file_list.append({'name': folder.get('Prefix').split('/')[-2], 'path': folder.get('Prefix'), 'is_folder': True, 'user' : user})
    if file_res:
        for file in file_res:
            file_list.append({'name': file.get('Key').split('/')[-1], 'path': file.get('Key'), 'is_folder': False, 'user':user})

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

def list_bucket():
    res = s3.list_buckets()
    return [bucket['Name'] for bucket in res['Buckets']]

def update_path(path, folder):
    return path + '/' + 'folder'
