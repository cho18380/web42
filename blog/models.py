from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add other fields as needed
    

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = RichTextField()
    image_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    overview = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.overview:
            self.overview = self.content[:200] + '...' # set overview to first 200 characters of content plus ellipsis
        super().save(*args, **kwargs)
