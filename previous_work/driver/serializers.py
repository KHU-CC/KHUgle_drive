from rest_framework import serializers
from .models import Article
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Article
        fields = (
            'id',
            'user',
            'title',
            'file',
            'content',
            'created_at',
            'updated_at',
            #'department_id',
        )
        read_only_fields = ('created_at', 'updated_at',)

# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = File
#         fields = (
#             'id',
#             'uploaded_at',
#             'updated_at',
#             'file',
#             'path',
#         )
#         read_only_fields = ('uploaded_at', 'updated_at')
