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
    aws_access_key_id='ASIAVJ7ZLDLC3WBHIK67',
    aws_secret_access_key='JI/5BZcuABgX5yHFwW9U3ftL+NMURf7KsfOBjRHA',
    aws_session_token='IQoJb3JpZ2luX2VjEMP//////////wEaCXVzLXdlc3QtMiJHMEUCIQCLWY2kGo9HVPafcaM2D2zyPfDcGNd3KdFXXBU/jMtqsQIgChLbur3gCv6PN122ItCRBTGwqTUQf9TeeetxIoDgS3oqqwIIbBAAGgwzNjUwNTgyNjc4NDUiDN0NQtnfDo+9wP1TciqIAiLkKg23gd4vA07frR4tUFiYF6nh3zCUsUD7AceJezs/qC84z2SB07Qdma357paPuk3+UE4I7vHjTtgvqatCFK1E7acSvlQcQ3j/s2L1TOsj9gj4ck21iDcLTfKVD8T5p3iE/uoQF9PQ1BVl3BDL9vFUdk7prkNdQAKwKEAfpSEIzDpO+kf2rUUdNBE3sQgTzquGDlYEa9CIvIYAJlE/tXcitV29MSdik0TeDlu1VLI+iIqeXkfgUXTKZP5qHax7TPlgRkw7YWeudKxUgBxkmueTXy1k1F5XfpSORrEx2hKGBdeKqbvY8nvAIjvCMoeota0XghOS5aZK1jJZDKapXnYKZblVzNNJvTDG0MaFBjqdAUHOvuqRBeUW/DHzJa60j5LuBfqYfpeoaZi9F7YnVLipyzZ8wFUXO/uIrcXEzeNgOUhBBCsZEg1jcCWR+Bp5qyD7+gLI5D1T0b3dUo5Ynwvet8snIUdjhINA3afvHgVX+yoW+5hID7ks0DMHQnnWklj8t1Xd16wVntGDM2OaWJ65i1hVMXB7T5EeD+HDHcKHKvwCMPpUwczENOBqs0w='
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
    response = s3.list_objects(Bucket=bucket, Prefix='', Delimiter='/')

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

def create_bucket(bucket, region=None):
    response = s3.create_bucket(Bucket=bucket)
    return response

def list_bucket():
    res = s3.list_buckets()
    return [bucket['Name'] for bucket in res['Buckets']]

def update_path(path, folder):
    return path + '/' + 'folder'
