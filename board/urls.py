from django.urls import path

from .views import *

app_name = 'board'

urlpatterns = [
    # base
    path('', home, name='index'),
    path('<int:post_id>/', detail, name='detail'),

    # post
    path('post/create/', post_create, name='post_create'),
    path('post/modify/<int:post_id>/', post_modify, name='post_modify'),
    path('post/delete/<int:post_id>/', post_delete, name='post_delete'),
    path('post/vote/<int:post_id>/', post_vote, name='post_vote'),

    # comment
    path('comment/create/<int:post_id>/', comment_create, name='comment_create'),
    path('comment/modify/<int:comment_id>/', comment_modify, name='comment_modify'),
    path('comment/delete/<int:comment_id>/', comment_delete, name='comment_delete'),
    path('comment/vote/<int:comment_id>/', comment_vote, name='comment_vote'),
]