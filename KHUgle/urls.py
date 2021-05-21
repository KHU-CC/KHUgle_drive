from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),       #KHUgle의 인덱스 페이지 --> view로 매핑
]