from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from board.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('board/', include('board.urls')),
    path('common/', include('common.urls')),
    path('', home, name='home'),  
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # media 경로 추가

#handler404 = 'common.views.page_not_found'