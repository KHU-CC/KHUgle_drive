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
    aws_access_key_id='ASIAVJ7ZLDLC56COFKSC',
    aws_secret_access_key='LkaYnyLuUpWXtQJGLO3pp2cWZipGKd5l1S/87tn2',
    aws_session_token='IQoJb3JpZ2luX2VjEBUaCXVzLXdlc3QtMiJHMEUCIFKBjpN6XsPWqWlyABzzSsfuiqSK6po6w1F8mEjHOYRbAiEA3NGQzv0pNDQkzb+ZsAooIvU28wPJD1xp8kXzd2yULXgqtAIIvv//////////ARAAGgwzNjUwNTgyNjc4NDUiDJwOa2JHIAS5CQFziiqIAmfzpxet4UBCe1nIpsoX62PhTsS+6TqEdfSBWqQ3tjKsDMs1V7wDDLdr9X+B3F1+GvbrWMOX0P/47SJY5tDwyr4GqN9IF12K6ALQ3W1hZ2Sd6XyXJGpGYS9dQmVVvDM2MwH/jCeONzCf7vdGJCXMa43Q2BQizUQefdZQtbXw9nqmzUjokNCY5GRQBmrZ52VGIE/IpOMEYBOgxVJDg7Qo2H4rUJYIEaYPz1r+XcxKlA8HEvjG9EyWJlHMwH3G4jO6HhGYw2VSia+HVpkJShR+oHw1knMN+cy8LH+RBgaz3XDenC4OhvTmnfWOxA8ZSzfw1LHQWUfLtLV3k+7k1gqbvhpGzezSLsj80zDA5diFBjqdAZyGU404dK+AVbcdhvHgyfpjaRvT4Mf6n8y3xX089gk1RsykFuzgo/VsLOnO0beaF0S0OdInltI93hEUIzXo2Qk2xEOnQI/AiH7d8DFDpnt+ddgoyQo141C3ic1xoIsyNSeMJE+Hkww1IUllpZlz7+X5tDRjUANiw7cD4PX8H3V57X3ftic0ETSzL4DJpCJUUV/vwjTfEhPMDvSncnI=',
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
