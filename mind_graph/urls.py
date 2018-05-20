from django.urls import path

from mind_graph import views

urlpatterns = [
    path('set_article_tags/', views.set_article_tags),
]
