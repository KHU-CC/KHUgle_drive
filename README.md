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
