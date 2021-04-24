from django.urls import path
from Driver import views

urlpatterns = [
    path('', views.index)
]
