from django.urls import path

from external_data_access import views

urlpatterns = [
    path('latest_articles/', views.get_latest_articles),
    path('not_indexed_articles/', views.get_not_indexed_articles),
]
