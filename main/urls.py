from django.urls import path
from main import views

urlpatterns = [
    path('section/subscribed/', views.get_subscribed_sections),
    path('section/created/', views.get_created_sections),
    path('section/hot/', views.get_hot_sections),
    path('section/new/', views.create_new_section),
    path('section/search/', views.search_for_sections),
    path('section/subscribe/', views.subscribe_section),
    path('section/unsubscribe/', views.unsubscribe_section),
    path('section/change/', views.change_section_detail),
    path('article/list/', views.get_article_list),
    path('article/content/', views.get_article_content),
    path('article/new/', views.publish_article),
    path('article/change/', views.change_article),
]
