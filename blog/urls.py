from django.urls import path
from .views import (
    PostDetailView,
    PostUpdateView,
    PostDeleteView
)
from . import views
from users.models import Poster

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('userposts/<int:pk>/',	views.user_posts, name='user-posts'),
    path('topicposts/<topic>/', views.topic_posts, name='topic-posts'),
    path('post/new/', views.create_post, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about')
]