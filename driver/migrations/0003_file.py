# Generated by Django 3.2.2 on 2021-05-11 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('driver', '0002_rename_author_article_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to='')),
            ],
        ),
    ]
