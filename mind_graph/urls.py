from django.urls import path

from mind_graph import views

urlpatterns = [
    path('', views.get_mind_graph),
    path('article_list/', views.get_mind_graph_article_list),
    path('set_article_tags/', views.set_article_tags),
]
