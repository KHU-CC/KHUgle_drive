# KHUgle_drive

## Start setup
1. python -m venv env
2. source env/bin/activate
3. pip install -r requirement.txt

## AWS credential setup (for AWS Educate)
$ aws configure   
aws_access_key_id = {aws_access_key_id}   
aws_secret_access_key = {aws_secret_access_key}  
$ cd ~/.aws   
$ vim credentials   
aws_session_token = {aws_session_token}   

## Run Server   
$ python manage.py migrate   
$ python manage.py runserver 0:8000   

## Dependancy
[LINK](https://github.com/KHU-CC/KHUgle_drive/blob/master/requirements.txt)   

## Team Members
* 기상윤   
* 김현기   
* 송재혁   
* 임태민   
* 최현준   
