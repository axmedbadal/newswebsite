# news/urls.py

from django.urls import path
from . import views  
urlpatterns = [
    path('', views.index, name='index',),
    path('article/<int:article_id>/', views.article_detail, name='article_detail'),
    path('article/<int:article_id>/add_comment/', views.add_comment, name='add_comment'),
    path('article/<int:article_id>/like/', views.like, name='like'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
]
