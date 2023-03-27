from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    # base
    path('', home, name='home'),
    path('<int:post_id>/', post_detail, name='detail'),
    path('login/', login, name='login'),

    # post
    path('create/', post_create, name='post_create'),
    #path('post/modify/<int:post_id>/', post_modify, name='post_modify'),
    #path('post/delete/<int:post_id>/', post_delete, name='post_delete'),

    # comment
    #path('comment/create/<int:post_id>/', comment_create, name='comment_create'),
    #path('comment/modify/<int:comment_id>/', comment_modify, name='comment_modify'),
    #path('comment/delete/<int:comment_id>/', comment_delete, name='comment_delete'),

]