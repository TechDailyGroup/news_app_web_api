from django.urls import path
from main import views

urlpatterns = [
    path('section/subscribed/', views.get_subscribed_sections),
    path('section/created/', views.get_created_sections),
    path('section/hot/', views.get_hot_sections),
    path('section/new/', views.create_new_section),
    path('section/detail/', views.get_section_detail),
    path('section/search/', views.search_for_sections),
    path('section/subscribe/', views.subscribe_section),
    path('section/unsubscribe/', views.unsubscribe_section),
    path('section/change/', views.change_section_detail),
    path('section/change_icon/', views.change_section_icon),
    path('article/list/', views.get_article_list),
    path('article/search/', views.search_for_article),
    path('article/recommended/', views.get_recommended_article_list),
    path('article/similar_artilces/', views.get_similar_articles),
    path('article/content/', views.get_article_content),
    path('article/new/', views.publish_article),
    path('article/change/', views.change_article),
    path('article/comment/', views.get_comments),
    path('article/comment/new/', views.make_comment),
    path('article/like/', views.like_the_article),
    path('article/like_or_not/', views.user_like_article_or_not),
    path('article/liker/', views.get_likers),
    path('suggested_words/', views.get_suggested_words),
]
