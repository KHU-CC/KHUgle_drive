# KHUgle_drive
Main project repository

## Start setup
1. python -m venv env
2. source env/bin/activate
3. pip install -r requirement.txt

## AWS credential setup
$ cd ../   
$ mkdir .aws   
$ touch credentials.ini   
$ vim credentials.ini   

[default]   
aws_access_key_id = {aws_access_key_id}   
aws_secret_access_key = {aws_secret_access_key}   
aws_session_token = {aws_session_token}   

$ python manage.py migrate   
$ python manage.py runserver 0:8000   

## Dependancy
* asgiref==3.3.4   
* boto3==1.17.77   
* botocore==1.20.77   
* Django==3.2.3   
* django-extensions==3.1.3   
* django-storages==1.11.1   
* djangorestframework==3.12.4   
* jmespath==0.10.0   
* python-dateutil==2.8.1   
* pytz==2021.1   
* s3transfer==0.4.2   
* six==1.16.0   
* sqlparse==0.4.1   
* urllib3==1.26.4   

# Team Members
* 기상윤   
* 김현기   
* 송재혁   
* 임태민   
* 최현준   
