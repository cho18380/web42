from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

app_name = 'blog'

urlpatterns = [
    # base
    path('', home, name='home'),
    path('<int:post_id>/', post_detail, name='detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # post
    path('create/', post_create, name='post_create'),
    #path('post/modify/<int:post_id>/', post_modify, name='post_modify'),
    #path('post/delete/<int:post_id>/', post_delete, name='post_delete'),

    # comment
    #path('comment/create/<int:post_id>/', comment_create, name='comment_create'),
    #path('comment/modify/<int:comment_id>/', comment_modify, name='comment_modify'),
    #path('comment/delete/<int:comment_id>/', comment_delete, name='comment_delete'),

]