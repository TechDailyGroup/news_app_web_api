from django.urls import path
from user_actions import views

urlpatterns = [
    path('score/', views.get_score),
    path('actions/', views.get_actions),
    path('rank/', views.get_rank),
]
