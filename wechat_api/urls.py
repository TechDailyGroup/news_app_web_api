from django.urls import path, include
from wechat_api import views

urlpatterns = [
    path('login/', views.wechat_login),
]
