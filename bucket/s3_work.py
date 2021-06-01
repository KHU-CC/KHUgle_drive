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
    aws_access_key_id='ASIAVJ7ZLDLC4TKQBLXL',
    aws_secret_access_key='mBDnxlD4EYEIfM4pWrmsyZ1u9p5s/tfBbHPQ083J',
    aws_session_token='IQoJb3JpZ2luX2VjEBAaCXVzLXdlc3QtMiJIMEYCIQC3CEog4vO1hjwq+i+24CpdxNwGqHJdWXGFRIeuVt4segIhAP5OsEPfIxVZbDTU5kQErIvZa5n4io3Xk3ejrb6yc1dzKrQCCLn//////////wEQABoMMzY1MDU4MjY3ODQ1IgwPE6XFLjeoGDqzCowqiALOXvM3A6q/I8+DRbS2IqyEJ4bfWXz2YUGs021yKLebhjEJ6cDDQ4h22EaiVmFm/2vxlKOnB1xJzdff4nKKdxkYdvJdG7bt3ucO+PlePVj1Ce55mi/wVxA/HhmqkQ/aPG9h/SoDLAbwdhUjksl2bRbzgpAv978cxwaXq5oSSbrHPuI1I4byEXQSXDHta5A8gjjsyHTSGl6XtVjOsaLp2gVgbehz5opWjfYRkRpNCkaHXjAfbQBNIysQWqxNfCtK/WYYPTzqAlCabNroeoeJfQILug9Qzlwg1zjuKx8ypkcjiivep1sS8zkffN5AXctNI9DeCMFS90It6hoy7VBfnfCayQdVHgh5FP8wxsHXhQY6nAEIaW6mxI/Vj+GR1HKVffephKBPJw6Hhs3eVzr3VxKxfOxuE31QcHjaZyV+vMinrc/+Qcce6XrAHmUtGMJ++PbXLnfP3oj+Ld/t5ucps0MsAUSRC92NEXi6E5blGJWGG6RS/F5GCAAQgGO0anZDKaEMjbITokqdGox+xcHzTc5pthdShYfQ3xxacX8hU/Bw3Jy+y7+9Kl/ebLQAMDY=',
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
