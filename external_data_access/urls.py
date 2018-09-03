from django.urls import path

from external_data_access import views

urlpatterns = [
    path('latest_articles/', views.get_latest_articles),
    path('article/list/', views.get_article_list),
]
