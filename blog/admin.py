from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title']


admin.site.register(Post, PostAdmin)

