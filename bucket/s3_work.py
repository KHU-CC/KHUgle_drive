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
    aws_access_key_id='ASIAVJ7ZLDLC47Z34S54',
    aws_secret_access_key='tpZEVOUeQBoKhc0Vta6x4gAoWSeJAwo9dCUmSoxL',
    aws_session_token='IQoJb3JpZ2luX2VjEMb//////////wEaCXVzLXdlc3QtMiJHMEUCIQDbrcxDupdnH+IYCv8HQ472HeGG5TV+xjNnNBUf8Ynu9AIgBOZzX+zK9fhhFtCpVVgyYyAR6fp1A/elDV393DKU/8oqqwIIbxAAGgwzNjUwNTgyNjc4NDUiDGwzRvFOvEG787HmVCqIArLrrMLBCOaKabLwCObv+VtUqPu1vk9+AlkhaL2NY/BvL2HY2HtbAS+If3BSC1iUofuaA+7p8gCGAcFE0nsdCa2Pm9/D92FFbTOo5cx8CtGm/TIkocOeT87bzDWNU57HCPwdnH1vSADhDgc5f+hkrW3xqN4zbPRFFbLKoDSZjdl2xLaKaU1u80cWZguBM+RUhh4LaaDmtP4jpIyUQaB2IPt71Sufl/q0oRDnUGGxccnF/YyDPruj5pwPy7Gmx+kZ8RXMLUt/RrweUPYDMwgBEqNxsZzRUnfvqZDsuoPxJav5nr4hCdOtv0nJ3RBytDYyA1GnykHyIAWCz1mfxD8yDXbXcAB3OjE1pjCRp8eFBjqdAVIi+PNaHXZu25he0TDVEpM5j5t+NT31bayckC2L7Nr+bFOjWP3x0WkHaBsk1FnFj5zkpLuVHOrU5VbyUY7E7bYgFSBE+kRR5xUrC3kDO1gNhPTrek5V8++4aYwd2s15a7P2cRYGU6BD2OZ9Y7nlZXW6OtWmAuorg9w3FHQ3x7JGclZ2JdArXeReL3BV1zF4vPfsvoJoy5G8gssx4Oo=',
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

def create_bucket(bucket):
    response = s3.create_bucket(Bucket=bucket)
    return response

def list_bucket():
    res = s3.list_buckets()
    return [bucket['Name'] for bucket in res['Buckets']]

def update_path(path, folder):
    return path + '/' + 'folder'
