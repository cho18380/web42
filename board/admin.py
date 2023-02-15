from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    search_fields = ['subject']

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['title']


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)