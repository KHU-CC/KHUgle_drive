"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from KHUgle import views

urlpatterns = [
    path('',views.index, name='index'),                 #초기 페이지인데 새로 만들어줘야한다. Settings의 LOGIN/LOGOUT REDIRECT도 고려
    path('admin/', admin.site.urls),
    path('KHUgle/', include('KHUgle.urls')),
    path('account/', include('account.urls')),
    #path('bucket/', include('bucket.urls')),
]
