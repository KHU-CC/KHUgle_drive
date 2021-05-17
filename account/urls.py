from django.urls import path, include
from django.contrib.auth import views as auth_views
from account.views import *
from account.models import *
from . import views

app_name = 'account'

urlpatterns = [
    path('privatePage', privatePage),
    path('groupPage', groupPage),
    path('groupCommunityPage', groupCommunityPage),
    path('userProofile', userProfilePage),

    # path('login', auth_views.LoginView.as_view(template_name='account/login.html'), name='loginPage'),
    path('login', CustomLogin.as_view(template_name='account/login.html'), name='loginPage'),
    # path('logout', auth_views.LogoutView.as_view(), name='logoutPage'),
    path('logout', CustomLogout.as_view(), name='logoutPage'),
    path('signup', views.signup, name='signup')
]



# from django.urls import path, include

#     path('account/login', loginPage),
#     # path('account/privatePage/<int:studentID>', privatePage)
#     path('account/privatePage', privatePage),
#     # path('account/groupPage/<int:course>', groupPage),
#     path('account/groupPage', groupPage),
#     path('account/signUp', SignUpView.as_view()),