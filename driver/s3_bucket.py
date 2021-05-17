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
    aws_access_key_id='ASIAVJ7ZLDLC5QVI57WO',
    aws_secret_access_key='lYR7Ute0YeGAKj2aWFVp0mBUZ7dXhQmwHiE+HN0C',
    aws_session_token='IQoJb3JpZ2luX2VjEJL//////////wEaCXVzLXdlc3QtMiJGMEQCIGSvj9XwfVYiEWCwVsbfC+5RNGFdvsGUAXAP7ICcSNAOAiA8oB4w6q1AGJfeAVc/2+/xtRFVIAYjRDjyopY4aP6UJiqrAggrEAAaDDM2NTA1ODI2Nzg0NSIMhHQ4xuNl8X8nswBIKogCJ7Ttx0QRiG1XpahSHq7N5IUn6LhPyR1EC+BYKSo34mjpqY4MFG7VDzB9PbO0X3Ef8JdWXWHjVaEmHdgqbHgrHuAhC7cO5YPiZOHD6qT9uyF95UcfejvnQPD/CT6vsqBAF6WCDxyXc7U8hKgk/T2Fbt5s+iZU5AZ2vL1GTBv/hGZ5XI4aTIAaM1YTJzwY+gA/apno/F9OREFpKr0J5Tc3SG00g2lk6Gb4/VfekCAG/sGZ4LxYM7088YsbEnBFT091DRit1zUqVb1cePX2JVI7CJwWifpm7SCGQCkw6RYBfK1Yz/Vh3JycC+YaRTFYh+IFnqJtOaSr5VWX6qu3I1UWBodRG0RppRpaMMDTg4UGOp4BQZRUdT8w45Fa2lsghMW98Abr0EbNSxav9EKHFt+N/MkwjgbgHwhEAnm4svcXOePlheoRBCDK3ycPqmgLnomcZ8EwW88wPJ/ZfXchjMzSEqC8goAQgQl2Eo/QWtX3lcUPEADTEwVJygBHc4mp/GvMZ83X18leA8JLy6yLu6Vc3qUHn76MAF1wYnlWyRBzA4RXZhCw0nFe67iQ0WaqI/0='
)

BUCKET = 'khugle-drive-test'

def upload_file(file_name, bucket, object_name=None):
    
    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name
    # Upload the fil
    response = s3.upload_file(file_name, bucket, object_name)

def create_bucket(bucket_name, region=None):
    s3.create_bucket(Bucket=bucket_name)

def list_bucket():
    res = s3.list_buckets()
    return [bucket['Name'] for bucket in res['Buckets']]

res = upload_file('C:\\Users\\dizzi\\Desktop\\KHUgle_drive\\static\\driver\\file\\text.txt', 'khugle-drive-test', 'image/test4.txt')

#res = upload_file(os.path.join(MEDIA_DIR, 'text.txt'), 'khugle-drive-test', 'image/test.txt')