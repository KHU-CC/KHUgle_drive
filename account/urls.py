from django.urls import path
from django.contrib.auth import views as auth_views
<<<<<<< HEAD
from KHUgle import views
=======
from KHUgle import views as KHUgle_views
from . import views
>>>>>>> master

app_name = 'account'

urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name='index'),        #로그인 성공 후 redirect 되는 경로는 KHUgle
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    #로그인, 로그아웃 경로는 settings.py에 설정
=======
    path('', KHUgle_views.index, name='index'),        #로그인 성공 후 redirect 되는 경로는 KHUgle
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),    #로그인, 로그아웃 경로는 settings.py에 설정
    path('signup/', views.signup, name='signup'),
>>>>>>> master
]