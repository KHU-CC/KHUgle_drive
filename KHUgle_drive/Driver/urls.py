from django.urls import path
from Driver import views

urlpatterns = [
    path('', views.index),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('private/', views.PrivateView.as_view(), name='private'),
    path('group/', views.GroupView.as_view(), name='group'),
    path('community/', views.CommunityView.as_view(), name='community'),
    path('community/<int:pk>', views.CommunityDetailView.as_view(), name='community-detail')
]
