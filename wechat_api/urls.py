from django.urls import path, include
from wechat_api import views

urlpatterns = [
    path('login/', views.wechat_login),
    path('upload_picture/', views.upload_picture),
]
