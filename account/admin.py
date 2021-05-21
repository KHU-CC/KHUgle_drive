from django.contrib import admin
from .models import CustomUser                


admin.site.register(CustomUser)               #admin에서 CustomUser model 관리