from django.contrib import admin
from django.urls import path, include

from board.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', include('board.urls')),
    #path('common/', include('common.urls')),
    path('', home, name='home'),  # '/' 에 해당되는 path
]

#handler404 = 'common.views.page_not_found'