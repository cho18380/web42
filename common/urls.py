from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'common'

urlpatterns = [
    #path('', home, name='index'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='login.html'), name='logout'),

]