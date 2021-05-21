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
    aws_access_key_id='ASIAVJ7ZLDLCQXGUGFZW',
    aws_secret_access_key='iUHJgKpv7cX/7iaIZN/OpDaH8kHVj+WlCqpC5rpa',
    aws_session_token='IQoJb3JpZ2luX2VjEBQaCXVzLXdlc3QtMiJGMEQCIFX7qh+zeFHuqUgSk8dTosRusGKmmONasuysHxxnE2zNAiAm8pdLdDNPL9f7PvpAkosv9V0iuVHk1rtr02jDQ2edVCq0Agit//////////8BEAAaDDM2NTA1ODI2Nzg0NSIMZBccbjvpSHMjq2rIKogCT/F3/EAnDqT72VcmOz6qb9VzllO5g/icGufBfxcxVBTg270JX+ozMSjSZC+Y3gAy3OMmlw8KVvymmbEsbRp89F5P39UFtAYOTSE4T6WLIQE7MaafRgl8JbxJtmDVwDMOritECaejDQSg2PsJ02Ctk2FeOn6JVhlf7bzgFRU4B12oxHeXQb6srFh0CEnn6j+zx2Ecg67ZWPVf0v5Uwztg6+oci5mU3p0AphA47pfkcb0cl3zA0m/a4JeYc1jqfUcEiXiXsH6XlR9J2vos4t8p73fi62RCSpfi0/+xXLITo5NM1dYkAyEEyAuTlEP0Banay4qa6PZRefq5XVNpwWUf/SzVBDcE4swSMISboIUGOp4Bhiw9XZvXd37weIz1sV3G9XO6BjNciOhU3xLQs5Wj7zJ08CPWZr2cJZ9BMdFekssTynM3+WVuq1vUXcprCuLN8Eqlli+0aC77HUjQwrRSoNM7ZoXLBruZoDsNE27xSQ/9SJHjSQuanQSm6IeufevZ1eMq5zPK5nNxFGA6EFLslNCnXHbwF7x69gMJgsRP3XII3qtr8WFxW+rJnp4dVJg='
)

BUCKET = 'khugle-drive-test'

def upload_file(file_name, bucket, file_path=None):
    
    # If S3 object_name was not specified, use file_name
    if file_path is None:
        file_path= file_name
    # Upload the fil
    response = s3.upload_file(file_name, bucket, file_path)
    return response

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

def create_bucket(bucket_name, region=None):
    response = s3.create_bucket(Bucket=bucket_name)
    return response

def list_bucket():
    res = s3.list_buckets()
    return [bucket['Name'] for bucket in res['Buckets']]

def split_path(path):
    return path.split('/')
